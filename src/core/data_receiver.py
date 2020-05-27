import os
import socketserver
import threading
import tkinter
from tkinter import messagebox

from src.utils.constants import SEPARATOR, BUFFER_SIZE
from src.core import encryption


class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUFFER_SIZE).decode()
        root = tkinter.Tk()
        root.withdraw()
        if SEPARATOR in data:
            self._handle_file(data)
        else:
            self._handle_message(data)

    def _handle_message(self, message):
        messagebox.showinfo(title="Received a message", message=f"New message:\n{message}")

    def _handle_file(self, header):
        filename, filesize = header.split(SEPARATOR)
        filename = os.path.basename(filename)

        if filename.endswith(".pem"):
            file_path = os.path.join(os.pardir, "keys", "public")
            filename = "receiver.pem"
        else:
            file_path = os.path.join(os.pardir, "downloads")
        if not os.path.exists(file_path):
            os.mkdir(file_path)

        with open(os.path.join(file_path, filename), "wb") as file:
            while True:
                bytes_read = self.request.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                file.write(bytes_read)

        if filename != "receiver.pem":
            encryption.decrypt_data(os.path.join(file_path, filename))

        messagebox.showinfo(title="Received a file", message=f"New file: {filename}")


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
