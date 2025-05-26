from cryptography.fernet import Fernet
import base64
import os

class CryptoManager:
    def __init__(self):
        self.key = Fernet.generate_key()
