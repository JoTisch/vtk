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


def vtk_visualize_pw(isource,
					 planes,
					 ilut=None,
					 name=None,
):

	def syncPlane(obj, event):
		value = int(obj.GetSliceIndex())
		planes[0].SetSliceIndex(value)

	renderWindow = vtk.vtkRenderWindow()
	renderer = vtk.vtkRenderer()
	renderer.ResetCamera()
	renderer.ResetCameraClippingRange()
	renderWindow.AddRenderer(renderer)

	iren = vtk.vtkRenderWindowInteractor()
	iren.SetRenderWindow(renderWindow)

	for i in range(0,len(isource)):
		planes[i].SetInteractor(iren)
		planes[i].SetLookupTable(ilut[i])
		planes[i].SetInputData(isource[i])
		planes[i].SetOrigin((0, 0, 0))
		planes[i].SetPlaneOrientationToZAxes()
		if i == 1:
			planes[i].AddObserver("InteractionEvent", syncPlane)
		planes[i].UpdatePlacement()
		planes[i].DisplayTextOn()
		planes[i].SetLeftButtonAction(1)
		planes[i].SetMiddleButtonAction(2)
		planes[i].SetRightButtonAction(0)
		planes[i].PlaceWidget()
		planes[i].On()

	renderer.SetBackground(0, 0, 0)
	renderWindow.SetSize(1280, 1024)
	renderWindow.SetWindowName(name)
	#renderer.SetBackground(0.1, 0.2, 0.4)

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
vtk_visualize(reader.GetOutputPort(), name="original image")
print('original: ', reader.GetOutput().GetPointData().GetScalars().GetRange())

min_value = min(reader.GetOutput().GetPointData().GetScalars().GetRange())
img_data = reader.GetOutput()

math = vtk.vtkImageMathematics()
math.SetInputData(img_data)
math.SetOperationToAddConstant()
math.SetConstantC(abs(min_value))
math.Update()

shifted = vtk.vtkImageData()
shifted.DeepCopy(math.GetOutput())

print('shifted: ', shifted.GetPointData().GetScalars().GetRange())

labelvalue = max(shifted.GetPointData().GetScalars().GetRange())
background = min(shifted.GetPointData().GetScalars().GetRange())
thresh = vtk.vtkImageThreshold()
thresh.SetInputData(img_data)
thresh.ThresholdBetween(200,900)
thresh.SetOutValue(background)
#thresh.SetInValue(labelvalue)
thresh.SetOutputScalarType(img_data.GetScalarType())
thresh.Update()

vtk_visualize(source=thresh.GetOutputPort(), name="threshold")
print('threshold: ', thresh.GetOutput().GetPointData().GetScalars().GetRange())

lut = vtk.vtkLookupTable()
lut.SetHueRange(0.0, 0.1)
lut.SetAlphaRange(0,1)
lut.Build()

plane = []
plane.append(vtk.vtkImagePlaneWidget())
plane.append(vtk.vtkImagePlaneWidget())

vtk_visualize_pw(planes=plane, isource=(reader.GetOutput(), thresh.GetOutput()),ilut=(None,lut),name="Segmentation")

