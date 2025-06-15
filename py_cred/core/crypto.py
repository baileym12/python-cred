from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class CryptoManager:
    def __init__(self, master_key=None):
        self._master_key = master_key
        self._salt = os.urandom(16)
        self._key = self._derive_key()

    def _derive_key(self):
        if not self._master_key:
            return Fernet.generate_key()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self._salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(self._master_key.encode()))

    def encrypt(self, data):
        f = Fernet(self._key)
        return f.encrypt(data.encode())

    def decrypt(self, encrypted_data):
        f = Fernet(self._key)
        return f.decrypt(encrypted_data).decode()

    @classmethod
    def generate_master_key(cls):
        """Generate a new master key."""
        return base64.urlsafe_b64encode(os.urandom(32)).decode()
