from Cryptodome.Cipher.AES import MODE_ECB, MODE_CBC, MODE_CFB, MODE_OFB
from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton, QLabel, QGridLayout, QProgressBar, \
    QRadioButton, QLineEdit, QPlainTextEdit
import os

from src.core.connection_config import ConnectionConfig
from src.core.data_receiver import DataReceiver
from src.core.data_sender import DataSender
from src.core import encryption
from src.utils.constants import MESSAGE


class ConfigApp(QWidget):
    def __init__(self):
        super().__init__()
        self.config = ConnectionConfig()
        self.access_key = ''
        self.layout = QGridLayout()
        self.layout.setSpacing(10)
        self.sender_ip_textbox = QLineEdit()
        self.sender_ip_textbox.setText("25.119.38.155")
        self.receiver_ip_textbox = QLineEdit()
        self.receiver_ip_textbox.setText("25.143.96.131")
        self.access_key_textbox = QLineEdit()
        self.sender_ip_label = QLabel("Provide your IP address:")
        self.receiver_ip_label = QLabel("Provide receiver's IP address:")
        self.access_key_label = QLabel("Please provide an access key, which will be used to encrypt RSA key:")
        self.confirm_button = QPushButton('Confirm')
        self._add_widgets()

        self.setLayout(self.layout)
        self.setGeometry(1000, 600, 200, 100)
        self.setWindowTitle('Welcome!')
        self.confirm_button.clicked.connect(self._confirm_click)
        self.show()

    def _confirm_click(self):
        self.access_key = self.access_key_textbox.text()
        self.config.access_key = self.access_key
        self.config.sender_ip = self.sender_ip_textbox.text()
        self.config.receiver_ip = self.receiver_ip_textbox.text()
        self.hide()
        self.main_app = MainApp(self.config, self.access_key)

    def _add_widgets(self):
        self.layout.addWidget(self.sender_ip_label, 0, 0)
        self.layout.addWidget(self.receiver_ip_label, 0, 1)
        self.layout.addWidget(self.sender_ip_textbox, 1, 0)
        self.layout.addWidget(self.receiver_ip_textbox, 1, 1)
        self.layout.addWidget(self.access_key_label, 2, 0)
        self.layout.addWidget(self.access_key_textbox, 3, 0)
        self.layout.addWidget(self.confirm_button, 4, 0)


class MainApp(QWidget):
    def __init__(self, config, access_key):
        super().__init__()
        self.encryption_mode = MODE_ECB
        self.file_path = ""
        self.access_key = access_key
        self.config = config
        self.data_sender = DataSender(config)
        self.data_receiver = DataReceiver(config, access_key)
        self.data_receiver.start_receiving()
        self.layout = QGridLayout()
        self.layout.setSpacing(10)
        self.browse_button = QPushButton('Browse')
        self.send_file_button = QPushButton('Send file')
        self.send_message_button = QPushButton("Send message")
        self.exchange_keys_button = QPushButton("Exchange keys")
        self.radio_button_ecb = QRadioButton('ECB')
        self.radio_button_cbc = QRadioButton('CBC')
        self.radio_button_cfb = QRadioButton('CFB')
        self.radio_button_ofb = QRadioButton('OFB')
        self.progress_bar = QProgressBar()
        self.dynamic_message = QLabel('Please select mode and file')
        self.message_textbox = QPlainTextEdit()
        self._add_widgets()

        self.setLayout(self.layout)
        self.setGeometry(700, 400, 400, 200)
        self.setWindowTitle('Jakub Wlostowski & Tomasz Michalski')

        self.browse_button.clicked.connect(self._browse_files)
        self.send_file_button.clicked.connect(self._send_file)
        self.send_message_button.clicked.connect(self._send_message)
        self.exchange_keys_button.clicked.connect(self._exchange_keys)
        self.radio_button_ecb.setChecked(True)
        self.radio_button_ecb.toggled.connect(self._set_encryption_mode)
        self.radio_button_cbc.toggled.connect(self._set_encryption_mode)
        self.radio_button_cfb.toggled.connect(self._set_encryption_mode)
        self.radio_button_ofb.toggled.connect(self._set_encryption_mode)

        self.show()

    def _browse_files(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        self.dynamic_message.setText(f"Selected file:\n{path}")
        self.file_path = path

    def _add_widgets(self):
        self.layout.addWidget(self.browse_button, 4, 3)
        self.layout.addWidget(self.send_file_button, 4, 4)
        self.layout.addWidget(self.exchange_keys_button, 3, 3)
        self.layout.addWidget(self.progress_bar, 0, 0, 1, 0)
        self.layout.addWidget(self.radio_button_ecb, 1, 0)
        self.layout.addWidget(self.radio_button_cbc, 2, 0)
        self.layout.addWidget(self.radio_button_cfb, 3, 0)
        self.layout.addWidget(self.radio_button_ofb, 4, 0)
        self.layout.addWidget(self.dynamic_message, 1, 1, 1, 3)
        self.layout.addWidget(self.message_textbox, 5, 0, 5, 4)
        self.layout.addWidget(self.send_message_button, 5, 4)

    def _send_file(self):
        if self.file_path == "":
            self.dynamic_message.setText("Select file to send")
            return
        encrypted_file = encryption.encrypt_file(self.file_path, self.encryption_mode)
        original_name = os.path.basename(self.file_path)
        self.data_sender.send_file(encrypted_file, original_name, self.progress_bar)

    def _send_message(self):
        message = self.message_textbox.toPlainText()
        encrypted_file = encryption.encrypt_message(message, self.encryption_mode)
        self.data_sender.send_file(encrypted_file, MESSAGE, self.progress_bar)

    def _set_encryption_mode(self):
        text = self.sender().text()
        if text == "ECB":
            self.encryption_mode = MODE_ECB
        if text == "CBC":
            self.encryption_mode = MODE_CBC
        if text == "CFB":
            self.encryption_mode = MODE_CFB
        if text == "OFB":
            self.encryption_mode = MODE_OFB

    def _exchange_keys(self):
        encryption.generate_private_and_public_keys(self.access_key)
        self.data_sender.send_file(os.path.join(os.pardir, "keys", "public", "my_public.pem"), "my_public.pem", self.progress_bar)
