import os
import socketserver
import threading

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout
from src.utils.constants import SEPARATOR, BUFFER_SIZE


class ReceivedWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.layout.setSpacing(10)
        self.proceed_button = QPushButton("Ok")
        self.message_received = QLabel("Placeholder")

        self.setLayout(self.layout)
        self.setGeometry(700, 400, 300, 100)
        self.setWindowTitle('Received a file')
        self._add_widgets()

        self.proceed_button.clicked.connect(self._confirm_click)
        self.show()

    def _add_widgets(self):
        self.layout.addWidget(self.proceed_button, 1, 1, 1, 1)
        self.layout.addWidget(self.message_received, 0, 0)

    def _confirm_click(self):
        self.hide()


class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUFFER_SIZE).decode()
        if SEPARATOR in data:
            self._handle_file(data)
        else:
            self._handle_message(data)

        # window = ReceivedWindow()

    def _handle_message(self, message):
        print(f"Message: {message}")

    def _handle_file(self, header):
        filename, filesize = header.split(SEPARATOR)
        filename = os.path.basename(filename)

        downloads = os.path.join(os.pardir, "downloads")
        if not os.path.exists(downloads):
            os.mkdir(downloads)

        with open(os.path.join(os.pardir, "downloads", filename), "wb") as file:
            while True:
                bytes_read = self.request.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                file.write(bytes_read)
        # window = ReceivedWindow()
        return


class Server(socketserver.TCPServer):
    def __init__(self, server_address, handler_class=RequestHandler):
        print("Init of the server")
        socketserver.TCPServer.__init__(self, server_address, handler_class)
        return


class DataReceiver:
    def __init__(self, config):
        self.address = (config.sender_ip, config.connection_port)
        self.server = Server(self.address, RequestHandler)

    def start_receiving(self):
        rcv_thread = threading.Thread(target=self.server.serve_forever)
        rcv_thread.setDaemon(True)
        rcv_thread.start()

    def stop_receiving(self):
        self.server.shutdown()
        self.server.socket.close()
