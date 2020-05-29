import os
import hashlib
import tempfile
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES, PKCS1_OAEP
import tkinter
from tkinter import messagebox

def hash_access_key(key):
    return str(hashlib.sha256(key.encode()).hexdigest())


def generate_private_and_public_keys(access_key):
    private_dir = os.path.join(os.pardir, "keys", "private")
    public_dir = os.path.join(os.pardir, "keys", "public")
    _create_directories_for_keys(private_dir, public_dir)
    hashed_access_key = hash_access_key(access_key)

    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    with open(os.path.join(private_dir, "private.pem"), "wb") as private_key_file:
        private_key_file.write(private_key)
    with open(os.path.join(public_dir, "my_public.pem"), "wb") as public_key_file:
        public_key_file.write(public_key)


def _create_directories_for_keys(private_dir, public_dir):
    if not os.path.exists(private_dir):
        os.makedirs(private_dir)
    if not os.path.exists(public_dir):
        os.makedirs(public_dir)


def encrypt_message(message, mode):
    message = message.encode()
    return _encrypt_data(message, mode)


def encrypt_file(file_path, mode):
    with open(file_path, "rb") as file:
        return _encrypt_data(file.read(), mode)


def _encrypt_data(data, mode=AES.MODE_EAX):
    recipient_key_path = os.path.join(os.pardir, "keys", "public", "receiver.pem")
    encrypted_file = tempfile.mktemp()

    recipient_key = RSA.import_key(open(recipient_key_path).read())
    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)

    with open(encrypted_file, "wb") as file_out:
        [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
        file_out.close()

    return encrypted_file


def decrypt_data(encrypted_file):
    private_dir = os.path.join(os.pardir, "keys", "private", "private.pem")
    private_key = RSA.import_key(open(private_dir).read())

    with open(encrypted_file, "rb") as file_in:
        enc_session_key, nonce, tag, ciphertext = \
            [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    # TODO send and receive MODE_X
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)

    if os.path.basename(encrypted_file) == "message":
        messagebox.showinfo(title="Received a message", message=f"New message:\n{data}")

    with open(encrypted_file, "wb") as decrypted_file:
        decrypted_file.write(data)
