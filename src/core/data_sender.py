import socket
import logging

log = logging.getLogger(__name__)


class DataSender:
    def __init__(self, ip, port):
        self.address = (ip, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_data(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            log.info(f"Connecting to {self.address}")
            sock.connect(self.address)
            log.info(f"Sending {data}")
            sock.send(data)
