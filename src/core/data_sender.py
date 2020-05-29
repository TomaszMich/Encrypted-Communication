import socket
import os
import sys

from src.utils.constants import SEPARATOR, BUFFER_SIZE


class DataSender:
    def __init__(self, config):
        self.address = (config.receiver_ip, config.connection_port)

    def send_message(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.address)
            s.send(message.encode())

    def send_file(self, filename, progress_bar):
        if filename == "":
            print("Nie wybrano pliku")
            return
        file_size = os.path.getsize(filename)
        bytes_read_size = 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.address)
            s.send(f"{filename}{SEPARATOR}{file_size}".ljust(BUFFER_SIZE).encode())
            with open(filename, "rb") as file:
                while True:
                    bytes_read = file.read(BUFFER_SIZE)
                    bytes_read_size += sys.getsizeof(bytes_read)
                    progress_bar.setValue((bytes_read_size / file_size) * 100)
                    if not bytes_read:
                        break
                    s.sendall(bytes_read)
