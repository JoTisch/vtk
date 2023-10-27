import vtk


def vtk_visualize(source,
				  name
):
	"""
	:param source:
	:param name:
	:return:
	"""
	#Create an image actor to display the image
	imageActor = vtk.vtkImageActor()
	mapper = imageActor.GetMapper()
	#TODO: type of input
	if source is not None:
		mapper.SetInputConnection(source)
	else:
		mapper.SetInputConnection(source)
	# Setup renderer
	renderer = vtk.vtkRenderer()
	renderer.AddActor(imageActor)
	renderer.ResetCamera()
	renderer.ResetCameraClippingRange()

	# Setup render window
	renderWindow = vtk.vtkRenderWindow()
	renderWindow.AddRenderer(renderer)
	renderWindow.SetSize(1280, 1024)
	renderWindow.SetWindowName(name)

	# Setup render window interactor
	renderWindowInteractor = vtk.vtkRenderWindowInteractor()
	style = vtk.vtkInteractorStyleImage()
	renderWindowInteractor.SetInteractorStyle(style)

	# Render and start interaction
	renderWindowInteractor.SetRenderWindow(renderWindow)
	renderWindow.Render()
	renderWindowInteractor.Initialize()
	renderWindowInteractor.Start()

def syncPlane(obj, event):
	rep.GetPlane(plane)

def vtk_visualize_pw(isource,
					 ilut=None,
):

	renderWindow = vtk.vtkRenderWindow()
	renderer = vtk.vtkRenderer()
	renderWindow.AddRenderer(renderer)

	iren = vtk.vtkRenderWindowInteractor()
	iren.SetRenderWindow(renderWindow)

	planes = []
	for i in range(0,len(isource)):
		planes.append(vtk.vtkImagePlaneWidget())
		planes[i].SetInteractor(iren)
		if ilut[i] is not None:
			planes[i].SetLookupTable(ilut[i])
		planes[i].SetInputConnection(isource[i])
		planes[i].SetPlaneOrientationToXAxes()
		planes[i].AddObserver("InteractionEvent", syncPlane)
		planes[i].PlaceWidget()
		planes[i].On()

	renderer.SetBackground(1, 1, 1)
	renderWindow.SetSize(1280, 1024)
	renderer.SetBackground(0.1, 0.2, 0.4)

	iren.Initialize()
	renderWindow.Render()
	iren.Start()
"--------------------------------------------------------------------------------"
"--------------------------------------------------------------------------------"
#Relative path
path_image = "./Data_Assignment2/aneurysm.vti"

#Read the image
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName(path_image);
reader.Update();

#Print scalar range
print('original: ', reader.GetOutput().GetPointData().GetScalars().GetRange())

min_value = min(reader.GetOutput().GetPointData().GetScalars().GetRange())
img_data = reader.GetOutput()

math = vtk.vtkImageMathematics()
math.SetInputData(img_data)
math.SetOperationToAddConstant()
math.SetConstantC(abs(min_value))
math.Update()


labelvalue = 255
background = 0
thresh = vtk.vtkImageThreshold()
thresh.SetInputData(masterImageData)
thresh.ThresholdBetween(min, max)
thresh.SetInValue(labelvalue)
thresh.SetOutValue(background)
thresh.SetOutputScalarType(editedLabelmap.GetScalarType())
thresh.Update()