import vtk

def vtk_visualize(source,
				  name
):
	"""
	:param source: source of image --type: vtk.GetOutput()
	:param name: name of image -- type: str
	"""
	# TODO: Print name over image

	renderer = vtk.vtkRenderer()
	renderer.ResetCamera()
	renderer.ResetCameraClippingRange()
	renderer.SetBackground(0, 0, 0)

	renderWindow = vtk.vtkRenderWindow()
	renderWindow.AddRenderer(renderer)
	renderWindow.SetSize(1280, 1024)
	renderWindow.SetWindowName(name)

	iren = vtk.vtkRenderWindowInteractor()
	iren.SetRenderWindow(renderWindow)

	plane = vtk.vtkImagePlaneWidget()
	plane.SetInteractor(iren)
	plane.SetInputData(source)
	plane.SetOrigin((0, 0, 0))
	plane.SetPlaneOrientationToZAxes()
	plane.UpdatePlacement()
	plane.PlaceWidget()
	plane.On()

	iren.Initialize()
	renderWindow.Render()
	iren.Start()
	
def syncImgSeg(source,
			   planes,
			   lut=None,
			   name=None,
):
	"""
	:param source: source of image -- type: vtk.GetOutput()
	:param planes: vtkImagePlaneWidget() -- type: list
	:param lut: look-up table -- type: table
	:param name: name of image -- type: str
	"""

	def syncPlane(obj, event):
		"""
		:param obj: 
		:param event:
		"""
		value = int(obj.GetSliceIndex())
		planes[0].SetSliceIndex(value)

	renderWindow = vtk.vtkRenderWindow()
	renderer = vtk.vtkRenderer()
	renderer.ResetCamera()
	renderer.ResetCameraClippingRange()
	renderWindow.AddRenderer(renderer)

	iren = vtk.vtkRenderWindowInteractor()
	iren.SetRenderWindow(renderWindow)

	for i in range(0,len(source)):
		planes[i].SetInteractor(iren)
		planes[i].SetLookupTable(lut[i])
		planes[i].SetInputData(source[i])
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
vtk_visualize(reader.GetOutput(), name="original image")
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

vtk_visualize(source=thresh.GetOutput(), name="threshold")
print('threshold: ', thresh.GetOutput().GetPointData().GetScalars().GetRange())

lut = vtk.vtkLookupTable()
lut.SetHueRange(0.0, 0.1)
lut.SetAlphaRange(0,1)
lut.Build()

plane = []
plane.append(vtk.vtkImagePlaneWidget())
plane.append(vtk.vtkImagePlaneWidget())

syncImgSeg(planes=plane, source=(reader.GetOutput(), thresh.GetOutput()),lut=(None,lut),name="Segmentation")

