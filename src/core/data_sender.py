import socket
import logging
import os
import hashlib
from fsplit.filesplit import FileSplit

log = logging.getLogger(__name__)

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096


class DataSender:
    def __init__(self, config):
        self.address = (config.receiver_ip, config.connection_port)

    def send_message(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            log.info(f"Connecting to {self.address}")
            s.connect(self.address)
            log.info(f"Sending {message}")
            s.send(message.encode())

    def send_file(self, filename, progress_bar):
        file_size = os.path.getsize(filename)
        total_bytes_read = 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            log.info(f"Connecting to {self.address}")
            s.connect(self.address)
            s.send(f"{filename}{SEPARATOR}{file_size}".encode())
            with open(filename, "rb") as file:
                while True:
                    bytes_read = file.read(BUFFER_SIZE)
                    total_bytes_read += bytes_read
                    if not bytes_read:
                        break
                    s.sendall(bytes_read)
                    progress_bar.setValue((int(bytes_read) / total_bytes_read) * 100)

    def split_data(self, filename):
        fs = FileSplit(filename, 5)
        fs.split()

    def generate_session_key():
        random_key = os.urandom(16)
        return random_key

    def hash_access_key(key):
        return str(hashlib.sha256(key).hexdigest())

    def generate_private_key(passcode):
        from Cryptodome.PublicKey import RSA
        key = RSA.generate(2048)
        encrypted_key = key.export_key(passphrase=passcode, pkcs=8, protection="scryptAndAES128-CBC")
        dir_name = 'C:\private_key'
        try:
            os.mkdir(dir_name)
            with open('C:\private_key\private_key.bin', 'wb') as f:
                f.write(encrypted_key)
        except FileExistsError:
            with open('C:\private_key\private_key.bin', 'wb') as f:
                f.write(encrypted_key)

    def generate_public_key():
        from Cryptodome.PublicKey import RSA
        key = RSA.generate(2048)
        dir_name = 'C:\public_key'
        try:
            os.mkdir(dir_name)
            with open('C:\public_key\public_key.pem', 'wb') as f:
                f.write(key.publickey().export_key())
        except FileExistsError:
            with open('C:\public_key\public_key.pem', 'wb') as f:
                f.write(key.publickey().export_key())
