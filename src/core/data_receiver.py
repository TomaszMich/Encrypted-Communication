import socketserver
import threading

from .constants import SERVER_ADDRESS, SERVER_PORT


class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(4096)
        print(data)
        self.request.send("Received data".encode())
        return


class Server(socketserver.TCPServer):
    def __init__(self, server_address,
                 handler_class=RequestHandler,
                 ):
        print("Init of the server")
        socketserver.TCPServer.__init__(self, server_address,
                                        handler_class)
        return


class DataReceiver:
    def __init__(self):
        self.address = (SERVER_ADDRESS, SERVER_PORT)
        self.server = Server(self.address, RequestHandler)

    def start_receiving(self):
        rcv_thread = threading.Thread(target=self.server.serve_forever)
        rcv_thread.setDaemon(True)
        rcv_thread.start()

    def stop_receiving(self):
        self.server.shutdown()
        self.server.socket.close()
