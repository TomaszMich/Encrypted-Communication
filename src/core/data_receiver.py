import socketserver
import threading
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout


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
        data = self.request.recv(4096)
        # r = ReceivedWindow()
        # r.show()
        print(data)
        self.request.send("Received data".encode())
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
       # self.server.serve_forever()
        rcv_thread = threading.Thread(target=self.server.serve_forever)
        rcv_thread.setDaemon(True)
        rcv_thread.start()

    def stop_receiving(self):
        self.server.shutdown()
        self.server.socket.close()
