
import sys, time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication, QPushButton, QLabel, QGridLayout, QProgressBar, QRadioButton, QMessageBox, QLineEdit

class Gui(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.browseButton = QPushButton('Browse')
        self.sendButton = QPushButton('Send')
        self.progressBar = QProgressBar()
        self.radioButton1 = QRadioButton('ECB')
        self.radioButton2 = QRadioButton('CBC')
        self.radioButton3 = QRadioButton('CFB')
        self.radioButton4 = QRadioButton('OFB')
        self.currentMessage = QLabel('Please select mode and file')

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.browseButton, 4, 3)
        grid.addWidget(self.sendButton, 4, 4)
        grid.addWidget(self.progressBar, 0, 0, 1, 0)
        grid.addWidget(self.radioButton1, 1, 0)
        grid.addWidget(self.radioButton2, 2, 0)
        grid.addWidget(self.radioButton3, 3, 0)
        grid.addWidget(self.radioButton4, 4, 0)
        grid.addWidget(self.currentMessage, 1, 1, 1, 3)

        self.setLayout(grid)
        self.setGeometry(700, 400, 400, 200)
        self.setWindowTitle('Jakub Wlostowski & Tomasz Michalski')
        self.show()
        self.browseButton.clicked.connect(self.browseFiles)

    def browseFiles(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        self.currentMessage.setText(path)
        return path


class pop_up(QWidget):
    def __init__(self):
        super().__init__()
        self.key = ' '
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        self.textbox = QLineEdit()
        self.label = QLabel('Please enter your encryption key below')
        self.confirmButton = QPushButton('Confirm')
        grid.addWidget(self.label, 0, 0)
        grid.addWidget(self.textbox, 1, 0)
        grid.addWidget(self.confirmButton, 1, 1)
        self.setLayout(grid)
        self.setGeometry(700, 400, 400, 100)
        self.setWindowTitle('Welcome!')
        self.show()
        self.confirmButton.clicked.connect(self.confirm_click)

    def confirm_click(self):
        self.key = self.textbox.text()
        self.hide()
        self.gui = Gui()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    start = pop_up()
    sys.exit(app.exec_())
