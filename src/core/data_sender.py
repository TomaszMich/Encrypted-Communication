import socket
import logging
from fsplit.filesplit import FileSplit

log = logging.getLogger(__name__)


class DataSender:
    def __init__(self, config):
        self.address = (config.receiver_ip, config.connection_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_data(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            log.info(f"Connecting to {self.address}")
            sock.connect(self.address)
            log.info(f"Sending {data}")
            sock.send(data)

    def split_data(self, filename):
        fs = FileSplit(filename, 5)
        fs.split()
