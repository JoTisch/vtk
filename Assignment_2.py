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
	value = int(obj.GetSliceIndex())
	plane2.SetSliceIndex(value)

def vtk_visualize_pw(isource,
					 plane1,
					 plane2, 
					 ilut=None,
					 name=None,
):

	renderWindow = vtk.vtkRenderWindow()
	renderer = vtk.vtkRenderer()
	renderer.ResetCamera()
	renderer.ResetCameraClippingRange()
	renderWindow.AddRenderer(renderer)

	iren = vtk.vtkRenderWindowInteractor()
	iren.SetRenderWindow(renderWindow)

	plane1.SetInteractor(iren)
	plane1.SetLookupTable(ilut[0])
	plane1.SetInputData(isource[0])
	plane1.SetOrigin((0, 0, 0))
	plane1.SetPlaneOrientationToZAxes()
	plane1.AddObserver("InteractionEvent", syncPlane)
	plane1.UpdatePlacement()
	plane1.DisplayTextOn()
	plane1.SetLeftButtonAction(1)
	plane1.SetMiddleButtonAction(2)
	plane1.SetRightButtonAction(0)
	plane1.PlaceWidget()
	plane1.On()


	plane2.SetInteractor(iren)
	plane2.SetLookupTable(ilut[1])
	plane2.SetInputData(isource[1])
	plane2.SetOrigin((0, 0, 0))
	plane2.SetPlaneOrientationToZAxes()
	plane2.UpdatePlacement()
	plane2.DisplayTextOn()
	plane2.SetLeftButtonAction(1)
	plane2.SetMiddleButtonAction(2)
	plane2.SetRightButtonAction(0)
	plane2.PlaceWidget()
	plane2.On()

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

plane1 = vtk.vtkImagePlaneWidget()
plane2 = vtk.vtkImagePlaneWidget()

vtk_visualize_pw(plane1=plane1, plane2=plane2, isource=(reader.GetOutput(), thresh.GetOutput()),ilut=(None,lut),name="Segmentation")

