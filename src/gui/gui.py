# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bsk.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(738, 383)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(530, 200, 82, 17))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(530, 220, 82, 17))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_3.setGeometry(QtCore.QRect(530, 240, 82, 17))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_4.setGeometry(QtCore.QRect(530, 260, 82, 17))
        self.radioButton_4.setObjectName("radioButton_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(530, 290, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(100, 240, 371, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(530, 180, 71, 16))
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(340, 280, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(200, 280, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def browseFiles(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        return path

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Jakub Wlostowski | Tomasz Michalski"))
        self.radioButton.setText(_translate("MainWindow", "ECB"))
        self.radioButton_2.setText(_translate("MainWindow", "CBC"))
        self.radioButton_3.setText(_translate("MainWindow", "CFB"))
        self.radioButton_4.setText(_translate("MainWindow", "OFB"))
        self.pushButton.setText(_translate("MainWindow", "Confirm"))
        self.label.setText(_translate("MainWindow", "Choose mode:"))
        self.pushButton_2.setText(_translate("MainWindow", "Send"))
        self.pushButton_3.setText(_translate("MainWindow", "Browse"))
        self.pushButton_3.clicked.connect(self.browseFiles)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
