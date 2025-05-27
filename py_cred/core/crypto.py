from cryptography.fernet import Fernet
import base64
import os

class CryptoManager:
    def __init__(self):
        self._key = Fernet.generate_key()  # Fixed: made key private
