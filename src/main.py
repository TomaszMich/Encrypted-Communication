# from data_receiver import DataReceiver
# from data_sender import DataSender
from PyQt5.QtWidgets import QApplication
import sys
from gui.gui import ConfigApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    start = ConfigApp()
    sys.exit(app.exec_())


    # sender = DataSender("25.119.38.155", 8080)
    # sender.send_data("Test message".encode())
