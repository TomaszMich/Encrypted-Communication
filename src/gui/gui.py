# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bsk.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication, QPushButton, QLabel, QGridLayout, QProgressBar, QRadioButton


class Gui(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        browseButton = QPushButton('Browse')
        sendButton = QPushButton('Send')
        progressBar = QProgressBar()
        radioButton1 = QRadioButton('ECB')
        radioButton2 = QRadioButton('CBC')
        radioButton3 = QRadioButton('CFB')
        radioButton4 = QRadioButton('OFB')
        currentMessage = QLabel('Please select mode and file')

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(browseButton, 4, 3)
        grid.addWidget(sendButton, 4, 4)
        grid.addWidget(progressBar, 0, 0, 1, 0)
        grid.addWidget(radioButton1, 1, 0)
        grid.addWidget(radioButton2, 2, 0)
        grid.addWidget(radioButton3, 3, 0)
        grid.addWidget(radioButton4, 4, 0)
        grid.addWidget(currentMessage, 1, 1, 1, 3)

        self.setLayout(grid)
        self.setGeometry(700, 400, 400, 200)
        self.setWindowTitle('Jakub Wlostowski & Tomasz Michalski')
        self.show()
        browseButton.clicked.connect(self.browseFiles)

    def browseFiles(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        return path


if __name__ == "__main__":
    app = QApplication(sys.argv)
    g = Gui()
    sys.exit(app.exec_())
