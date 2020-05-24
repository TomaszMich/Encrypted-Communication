from Cryptodome.Cipher.AES import MODE_ECB, MODE_CBC, MODE_CFB, MODE_OFB
from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton, QLabel, QGridLayout, QProgressBar, \
    QRadioButton, QLineEdit, QPlainTextEdit

from src.core.connection_config import ConnectionConfig
from src.core.data_receiver import DataReceiver
from src.core.data_sender import DataSender


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
        self.receiver_ip_textbox.setText("25.66.64.255")
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
        self.config.sender_ip = self.sender_ip_textbox.text()
        self.config.receiver_ip = self.receiver_ip_textbox.text()
        self.hide()
        self.main_app = MainApp(self.config)

    def _add_widgets(self):
        self.layout.addWidget(self.sender_ip_label, 0, 0)
        self.layout.addWidget(self.receiver_ip_label, 0, 1)
        self.layout.addWidget(self.sender_ip_textbox, 1, 0)
        self.layout.addWidget(self.receiver_ip_textbox, 1, 1)
        self.layout.addWidget(self.access_key_label, 2, 0)
        self.layout.addWidget(self.access_key_textbox, 3, 0)
        self.layout.addWidget(self.confirm_button, 4, 0)


class MainApp(QWidget):
    def __init__(self, config):
        super().__init__()
        self.encryption_mode = MODE_ECB
        self.file_path = ""
        self.config = config
        self.data_sender = DataSender(config)
        self.data_receiver = DataReceiver(config)
        self.data_receiver.start_receiving()
        self.layout = QGridLayout()
        self.layout.setSpacing(10)
        self.browse_button = QPushButton('Browse')
        self.send_file_button = QPushButton('Send file')
        self.send_message_button = QPushButton("Send message")
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
        self.radio_button_ecb.setChecked(True)
        self.radio_button_ecb.mode = MODE_ECB
        self.radio_button_cbc.mode = MODE_CBC
        self.radio_button_cfb.mode = MODE_CFB
        self.radio_button_ofb.mode = MODE_OFB
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
        self.data_sender.send_file(self.file_path, self.progress_bar)

    def _send_message(self):
        message = self.message_textbox.toPlainText()
        self.data_sender.send_message(message)

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
