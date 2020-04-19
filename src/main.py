from PyQt5.QtWidgets import QApplication
import sys

from gui.gui import ConfigApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    start = ConfigApp()
    sys.exit(app.exec_())
