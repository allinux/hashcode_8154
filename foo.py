from PyQt5 import QtCore, QtWidgets,QtGui
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QFileDialog, QSlider
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PIL import Image
import sys

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 300)
        vs1=0

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(220, 0, 310, 310))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.frame1 = QtWidgets.QFrame(self.centralwidget)
        self.frame1.setGeometry(QtCore.QRect(550, 10, 310, 300))
        self.frame1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame1.setObjectName("frame1")


        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 171, 301))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")


        self.horizontalSlider = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.verticalLayout.addWidget(self.horizontalSlider)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setValue(vs1)
        self.horizontalSlider.setTickInterval(10)
        self.horizontalSlider.setTickPosition(QSlider.TicksBelow)
        self.horizontalSlider.setObjectName("horizontalSlider")
        #self.horizontalSlider.valueChanged.connect(self.valuechange)
        #self.horizontalSlider.bl

        #print(self.horizontalSlider.value)


        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)


        self.pushButton3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton3.setObjectName("pushButton3")
        self.verticalLayout.addWidget(self.pushButton3)

        self.pushButton2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton2.setObjectName("pushButton2")
        self.verticalLayout.addWidget(self.pushButton2)

        self.pushButton4 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton4.setObjectName("pushButton4")
        self.verticalLayout.addWidget(self.pushButton2)

        self.statusbar = self.statusBar()



        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 671, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        MainWindow.setCentralWidget(self.centralwidget)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        print(self.hasMouseTracking())

        self.show()

    

    def mousePressEvent(self, event):
        txt = "Mouse 위치 ; x={0},y={1}, MR 영상내 위치={2},{3}".format(event.x(), event.y(), event.x()-550, event.y()-10)
        self.statusbar.showMessage(txt)
        print(event.globalX())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "OpenVTK"))
        self.pushButton2.setText(_translate("MainWindow", "Close"))
        self.pushButton3.setText(_translate("MainWindow", "Change_Intensity"))
        self.pushButton4.setText(_translate("MainWindow", "Clear"))
