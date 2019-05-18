import sys

import vtk
from PyQt5 import Qt, QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from foo import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    '''
    '''
    def __init__(self, parent=None):  # 메인윈도우 띄우고
        super(MainWindow, self).__init__(parent)  # 메인윈도우 상속받고
        self.setupUi(self)  # setupui상속받고
        self.pushButton.clicked.connect(self.OpenVTK)
        # self.pushButton1.clicked.connect(self.ETC)
        self.pushButton2.clicked.connect(
            QtCore.QCoreApplication.instance().quit)
        self.pushButton3.clicked.connect(self.UsingFilter)
        self.pushButton4.clicked.connect(self.clear)

        self.horizontalSlider.sliderReleased.connect(self.valuechange)
        self.setMouseTracking(True)

    def clear(self):
        self.setupUi(self)  # setupui상속받고
        self.pushButton.clicked.connect(self.OpenVTK)
        # self.pushButton1.clicked.connect(self.ETC)
        self.pushButton2.clicked.connect(
            QtCore.QCoreApplication.instance().quit)
        self.pushButton3.clicked.connect(self.UsingFilter)
        self.pushButton4.clicked.connect(self.clear)
        self.horizontalSlider.sliderReleased.connect(self.valuechange)
        self.setMouseTracking(True)
        delattr(self, 'v2')

    count = 0
    def valuechange(self):

        self.count += 1
        print("Scroll Value", self.horizontalSlider.value())
        print("count", self.count)
        self.UsingFilter(self.horizontalSlider.value())

    def OpenVTK(self):
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl = Qt.QVBoxLayout()
        self.vl.addWidget(self.vtkWidget)

        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(
            self.ren)  # vtk widget에 렌더링할 ren을 넣어주고
        # 출력을 담당할 iren에 vtk widget정보를 입력
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        # renWin = vtk.vtkRenderWindow()
        # renWin.AddRenderer(self.ren)
        # self.iren = vtk.vtkRenderWindowInteractor()
        # self.iren.SetRenderWindow(renWin)
        # self.vtkWidget.GetRenderWindow().AddRenderer(self.ren) #vtk widget에 렌더링할 ren을 넣어주고
        # self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()#출력을 담당할 iren에 vtk widget정보를 입력

        # Create source
        colors = vtk.vtkNamedColors()
        colors.SetColor("SkinColor", [255, 125, 64, 255])
        colors.SetColor("BkgColor", [51, 77, 102, 255])

        reader = vtk.vtkMetaImageReader()
        reader.SetFileName('FullHead.mhd')
        reader.Update()

        skinExtractor = vtk.vtkMarchingCubes()
        skinExtractor.SetInputConnection(reader.GetOutputPort())
        skinExtractor.SetValue(0, 500)
        skinExtractor.Update()

        skinStripper = vtk.vtkStripper()
        skinStripper.SetInputConnection(skinExtractor.GetOutputPort())
        skinStripper.Update()

        skinMapper = vtk.vtkPolyDataMapper()
        skinMapper.SetInputConnection(skinStripper.GetOutputPort())
        skinMapper.ScalarVisibilityOff()

        skin = vtk.vtkActor()
        skin.SetMapper(skinMapper)
        skin.GetProperty().SetDiffuseColor(colors.GetColor3d("SkinColor"))
        skin.GetProperty().SetSpecular(.3)
        skin.GetProperty().SetSpecularPower(20)

        # An isosurface, or contour value of 1150 is known to correspond to
        # the bone of the patient.
        # The triangle stripper is used to create triangle
        # strips from the isosurface these render much faster on may
        # systems.
        boneExtractor = vtk.vtkMarchingCubes()
        boneExtractor.SetInputConnection(reader.GetOutputPort())
        boneExtractor.SetValue(0, 1150)

        boneStripper = vtk.vtkStripper()
        boneStripper.SetInputConnection(boneExtractor.GetOutputPort())

        boneMapper = vtk.vtkPolyDataMapper()
        boneMapper.SetInputConnection(boneStripper.GetOutputPort())
        boneMapper.ScalarVisibilityOff()

        bone = vtk.vtkActor()
        bone.SetMapper(boneMapper)
        bone.GetProperty().SetDiffuseColor(colors.GetColor3d("Ivory"))

        # An outline provides context around the data.
        #
        outlineData = vtk.vtkOutlineFilter()
        outlineData.SetInputConnection(reader.GetOutputPort())
        outlineData.Update()

        mapOutline = vtk.vtkPolyDataMapper()
        mapOutline.SetInputConnection(outlineData.GetOutputPort())

        outline = vtk.vtkActor()
        outline.SetMapper(mapOutline)
        outline.GetProperty().SetColor(colors.GetColor3d("White"))

        # Now we are creating three orthogonal planes passing through the
        # volume. Each plane uses a different texture map and therefore has
        # different coloration.

        # Start by creating a black/white lookup table.
        value = int(self.horizontalSlider.value()) * 30
        print(2000 + value)
        bwLut = vtk.vtkLookupTable()
        bwLut.SetTableRange(0, 2000+value)
        bwLut.SetSaturationRange(0, 0)
        bwLut.SetHueRange(0, 0)
        bwLut.SetValueRange(0, 1)
        bwLut.Build()  # effective built

        # Now create a lookup table that consists of the full hue circle
        # (from HSV).
        hueLut = vtk.vtkLookupTable()
        hueLut.SetTableRange(0, 2000)
        hueLut.SetHueRange(0, 0)
        hueLut.SetSaturationRange(1, 1)
        hueLut.SetValueRange(0, 1)
        hueLut.Build()  # effective built

        # Finally, create a lookup table with a single hue but having a range
        # in the saturation of the hue.

        satLut = vtk.vtkLookupTable()
        satLut.SetTableRange(0, 2000)
        satLut.SetHueRange(.6, .6)
        satLut.SetSaturationRange(0, 1)
        satLut.SetValueRange(1, 1)
        satLut.Build()  # effective built

        # Create the first of the three planes. The filter vtkImageMapToColors
        # maps the data through the corresponding lookup table created above.  The
        # vtkImageActor is a type of vtkProp and conveniently displays an image on
        # a single quadrilateral plane. It does this using texture mapping and as
        # a result is quite fast. (Note: the input image has to be unsigned char
        # values, which the vtkImageMapToColors produces.) Note also that by
        # specifying the DisplayExtent, the pipeline requests data of this extent
        # and the vtkImageMapToColors only processes a slice of data.
        sagittalColors = vtk.vtkImageMapToColors()
        sagittalColors.SetInputConnection(reader.GetOutputPort())
        sagittalColors.SetLookupTable(bwLut)
        sagittalColors.Update()

        sagittal = vtk.vtkImageActor()
        sagittal.GetMapper().SetInputConnection(sagittalColors.GetOutputPort())
        # 앞 두 파라미터로 Sagittal 의 위치조절
        sagittal.SetDisplayExtent(128, 128, 0, 255, 0, 92)

        # Create the second (axial) plane of the three planes. We use the
        # same approach as before except that the extent differs.
        axialColors = vtk.vtkImageMapToColors()
        axialColors.SetInputConnection(reader.GetOutputPort())
        axialColors.SetLookupTable(bwLut)
        axialColors.Update()
        axial = vtk.vtkImageActor()
        axial.GetMapper().SetInputConnection(axialColors.GetOutputPort())
        axial.SetDisplayExtent(0, 255, 0, 255, 46, 46)

        # Create the third (coronal) plane of the three planes. We use
        # the same approach as before except that the extent differs.
        coronalColors = vtk.vtkImageMapToColors()
        coronalColors.SetInputConnection(reader.GetOutputPort())
        coronalColors.SetLookupTable(bwLut)
        coronalColors.Update()

        coronal = vtk.vtkImageActor()
        coronal.GetMapper().SetInputConnection(coronalColors.GetOutputPort())
        coronal.SetDisplayExtent(0, 255, 128, 128, 0, 92)

        # It is convenient to create an initial view of the data. The
        # FocalPoint and Position form a vector direction. Later on
        # (ResetCamera() method) this vector is used to position the camera
        # to look at the data in this direction.
        aCamera = vtk.vtkCamera()
        aCamera.SetViewUp(0, 0, -1)
        aCamera.SetPosition(0, -1, 0)
        aCamera.SetFocalPoint(0, 0, 0)
        aCamera.ComputeViewPlaneNormal()
        aCamera.Azimuth(0.0)
        aCamera.Elevation(0.0)

        # Actors are added to the renderer.
        self.ren.AddActor(outline)
        self.ren.AddActor(sagittal)
        self.ren.AddActor(axial)
        self.ren.AddActor(coronal)
        # self.ren.AddActor(skin)
        # self.ren.AddActor(bone)

        # Turn off bone for this example.
        bone.VisibilityOn()

        # Set skin to semi-transparent.
        skin.GetProperty().SetOpacity(0.5)

        # An initial camera view is created.  The Dolly() method moves
        # the camera towards the FocalPoint, thereby enlarging the image.
        self.ren.SetActiveCamera(aCamera)

        # Calling Render() directly on a vtkRenderer is strictly forbidden.
        # Only calling Render() on the vtkRenderWindow is a valid call.
        # renWin.Render()
        self.show()

        self.ren.ResetCamera()
        self.frame.setLayout(self.vl)
        aCamera.Dolly(1.5)

        # Note that when camera movement occurs (as it does in the Dolly()
        # method), the clipping planes often need adjusting. Clipping planes
        # consist of two planes: near and far along the view direction. The
        # near plane clips out objects in front of the plane; the far plane
        # clips out objects behind the plane. This way only what is drawn
        # between the planes is actually rendered.
        self.ren.ResetCameraClippingRange()

        # Interact with the data.
        #     renWin.Render()
        self.show()
        self.iren.Initialize()
        self.iren.Start()

    def UsingFilter(self, value):
        
        if not hasattr(self, 'v2'):
            self.vtkWidget = QVTKRenderWindowInteractor(self.frame1)
            self.v2 = Qt.QVBoxLayout()
            self.v2.addWidget(self.vtkWidget)

            self.ren = vtk.vtkRenderer()
            self.vtkWidget.GetRenderWindow().AddRenderer(
                self.ren)  # vtk widget에 렌더링할 ren을 넣어주고
            # 출력을 담당할 iren에 vtk widget정보를 입력
            self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        # renWin = vtk.vtkRenderWindow()
        # renWin.AddRenderer(self.ren)
        # self.iren = vtk.vtkRenderWindowInteractor()
        # self.iren.SetRenderWindow(renWin)
        # self.vtkWidget.GetRenderWindow().AddRenderer(self.ren) #vtk widget에 렌더링할 ren을 넣어주고
        # self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()#출력을 담당할 iren에 vtk widget정보를 입력

        # Create source
        colors = vtk.vtkNamedColors()
        colors.SetColor("SkinColor", [255, 125, 64, 255])
        colors.SetColor("BkgColor", [51, 77, 102, 255])

        reader = vtk.vtkMetaImageReader()
        reader.SetFileName('FullHead.mhd')
        reader.Update()

        skinExtractor = vtk.vtkMarchingCubes()
        skinExtractor.SetInputConnection(reader.GetOutputPort())
        skinExtractor.SetValue(0, 500)
        skinExtractor.Update()

        skinStripper = vtk.vtkStripper()
        skinStripper.SetInputConnection(skinExtractor.GetOutputPort())
        skinStripper.Update()

        skinMapper = vtk.vtkPolyDataMapper()
        skinMapper.SetInputConnection(skinStripper.GetOutputPort())
        skinMapper.ScalarVisibilityOff()

        skin = vtk.vtkActor()
        skin.SetMapper(skinMapper)
        skin.GetProperty().SetDiffuseColor(colors.GetColor3d("SkinColor"))
        skin.GetProperty().SetSpecular(.3)
        skin.GetProperty().SetSpecularPower(20)

        # An isosurface, or contour value of 1150 is known to correspond to
        # the bone of the patient.
        # The triangle stripper is used to create triangle
        # strips from the isosurface these render much faster on may
        # systems.
        boneExtractor = vtk.vtkMarchingCubes()
        boneExtractor.SetInputConnection(reader.GetOutputPort())
        boneExtractor.SetValue(0, 1150)

        boneStripper = vtk.vtkStripper()
        boneStripper.SetInputConnection(boneExtractor.GetOutputPort())

        boneMapper = vtk.vtkPolyDataMapper()
        boneMapper.SetInputConnection(boneStripper.GetOutputPort())
        boneMapper.ScalarVisibilityOff()

        bone = vtk.vtkActor()
        bone.SetMapper(boneMapper)
        bone.GetProperty().SetDiffuseColor(colors.GetColor3d("Ivory"))

        # An outline provides context around the data.
        #
        outlineData = vtk.vtkOutlineFilter()
        outlineData.SetInputConnection(reader.GetOutputPort())
        outlineData.Update()

        mapOutline = vtk.vtkPolyDataMapper()
        mapOutline.SetInputConnection(outlineData.GetOutputPort())

        outline = vtk.vtkActor()
        outline.SetMapper(mapOutline)
        outline.GetProperty().SetColor(colors.GetColor3d("White"))

        # Now we are creating three orthogonal planes passing through the
        # volume. Each plane uses a different texture map and therefore has
        # different coloration.

        # Start by creating a black/white lookup table.
        value = int(self.horizontalSlider.value()) * 30
        print(2000 + value)
        bwLut = vtk.vtkLookupTable()
        bwLut.SetTableRange(0, 2000 + value)
        bwLut.SetSaturationRange(0, 0)
        bwLut.SetHueRange(0, 0)
        bwLut.SetValueRange(0, 1)
        bwLut.Build()  # effective built

        # Now create a lookup table that consists of the full hue circle
        # (from HSV).
        hueLut = vtk.vtkLookupTable()
        hueLut.SetTableRange(0, 2000)
        hueLut.SetHueRange(0, 0)
        hueLut.SetSaturationRange(1, 1)
        hueLut.SetValueRange(0, 1)
        hueLut.Build()  # effective built

        # Finally, create a lookup table with a single hue but having a range
        # in the saturation of the hue.

        satLut = vtk.vtkLookupTable()
        satLut.SetTableRange(0, 2000)
        satLut.SetHueRange(.6, .6)
        satLut.SetSaturationRange(0, 1)
        satLut.SetValueRange(1, 1)
        satLut.Build()  # effective built

        # Create the first of the three planes. The filter vtkImageMapToColors
        # maps the data through the corresponding lookup table created above.  The
        # vtkImageActor is a type of vtkProp and conveniently displays an image on
        # a single quadrilateral plane. It does this using texture mapping and as
        # a result is quite fast. (Note: the input image has to be unsigned char
        # values, which the vtkImageMapToColors produces.) Note also that by
        # specifying the DisplayExtent, the pipeline requests data of this extent
        # and the vtkImageMapToColors only processes a slice of data.
        sagittalColors = vtk.vtkImageMapToColors()
        sagittalColors.SetInputConnection(reader.GetOutputPort())
        sagittalColors.SetLookupTable(bwLut)
        sagittalColors.Update()

        sagittal = vtk.vtkImageActor()
        sagittal.GetMapper().SetInputConnection(sagittalColors.GetOutputPort())
        # 앞 두 파라미터로 Sagittal 의 위치조절
        sagittal.SetDisplayExtent(128, 128, 0, 255, 0, 92)

        # Create the second (axial) plane of the three planes. We use the
        # same approach as before except that the extent differs.
        axialColors = vtk.vtkImageMapToColors()
        axialColors.SetInputConnection(reader.GetOutputPort())
        axialColors.SetLookupTable(bwLut)
        axialColors.Update()
        axial = vtk.vtkImageActor()
        axial.GetMapper().SetInputConnection(axialColors.GetOutputPort())
        axial.SetDisplayExtent(0, 255, 0, 255, 46, 46)

        # Create the third (coronal) plane of the three planes. We use
        # the same approach as before except that the extent differs.
        coronalColors = vtk.vtkImageMapToColors()
        coronalColors.SetInputConnection(reader.GetOutputPort())
        coronalColors.SetLookupTable(bwLut)
        coronalColors.Update()

        coronal = vtk.vtkImageActor()
        coronal.GetMapper().SetInputConnection(coronalColors.GetOutputPort())
        coronal.SetDisplayExtent(0, 255, 128, 128, 0, 92)

        # It is convenient to create an initial view of the data. The
        # FocalPoint and Position form a vector direction. Later on
        # (ResetCamera() method) this vector is used to position the camera
        # to look at the data in this direction.
        aCamera = vtk.vtkCamera()
        aCamera.SetViewUp(0, 0, -1)
        aCamera.SetPosition(0, -1, 0)
        aCamera.SetFocalPoint(0, 0, 0)
        aCamera.ComputeViewPlaneNormal()
        aCamera.Azimuth(0.0)
        aCamera.Elevation(0.0)

        # Actors are added to the renderer.
        self.ren.AddActor(outline)
        self.ren.AddActor(sagittal)
        self.ren.AddActor(axial)
        self.ren.AddActor(coronal)
        # self.ren.AddActor(skin)
        # self.ren.AddActor(bone)
        # Turn off bone for this example.
        bone.VisibilityOn()

        # Set skin to semi-transparent.
        skin.GetProperty().SetOpacity(0.5)

        # An initial camera view is created.  The Dolly() method moves
        # the camera towards the FocalPoint, thereby enlarging the image.
        self.ren.SetActiveCamera(aCamera)

        # Calling Render() directly on a vtkRenderer is strictly forbidden.
        # Only calling Render() on the vtkRenderWindow is a valid call.
        # renWin.Render()
        self.show()

        self.ren.ResetCamera()
        self.frame1.setLayout(self.v2)
        aCamera.Dolly(1.5)

        # Note that when camera movement occurs (as it does in the Dolly()
        # method), the clipping planes often need adjusting. Clipping planes
        # consist of two planes: near and far along the view direction. The
        # near plane clips out objects in front of the plane; the far plane
        # clips out objects behind the plane. This way only what is drawn
        # between the planes is actually rendered.
        self.ren.ResetCameraClippingRange()

        # Interact with the data.
        #     renWin.Render()
        self.show()
        self.iren.Initialize()
        self.iren.Start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
