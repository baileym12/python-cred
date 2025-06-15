import os
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class CryptoManager:
    def __init__(self, master_key_path: str = ".master_key"):
        self.master_key_path = Path(master_key_path)
        self._load_or_create_master_key()

    def _load_or_create_master_key(self) -> None:
        """Load existing master key or create a new one."""
        if self.master_key_path.exists():
            with open(self.master_key_path, "rb") as f:
                self.master_key = f.read()
        else:
            self.master_key = self.generate_master_key()
            with open(self.master_key_path, "wb") as f:
                f.write(self.master_key)

    @classmethod
    def generate_master_key(cls) -> bytes:
        """Generate a new master key."""
        return Fernet.generate_key()

    def _get_fernet(self) -> Fernet:
        """Get a Fernet instance for encryption/decryption."""
        return Fernet(self.master_key)

    def encrypt(self, data: str) -> bytes:
        """Encrypt data using the master key."""
        if not isinstance(data, str):
            raise ValueError("Data must be a string")
        return self._get_fernet().encrypt(data.encode())

    def decrypt(self, encrypted_data: bytes) -> str:
        """Decrypt data using the master key."""
        if not isinstance(encrypted_data, bytes):
            raise ValueError("Encrypted data must be bytes")
        return self._get_fernet().decrypt(encrypted_data).decode()

    def rotate_master_key(self) -> None:
        """Rotate the master key and re-encrypt all secrets."""
        # Generate new master key
        new_master_key = self.generate_master_key()
        new_fernet = Fernet(new_master_key)

        # Save old key for re-encryption
        old_fernet = self._get_fernet()

        # Update master key
        self.master_key = new_master_key
        with open(self.master_key_path, "wb") as f:
            f.write(self.master_key)

        # Re-encrypt all secrets
        secrets_dir = Path(".secrets/secrets")
        if secrets_dir.exists():
            for secret_file in secrets_dir.glob("*.enc"):
                with open(secret_file, "rb") as f:
                    encrypted_data = f.read()
                
                # Decrypt with old key
                decrypted_data = old_fernet.decrypt(encrypted_data)
                
                # Encrypt with new key
                new_encrypted_data = new_fernet.encrypt(decrypted_data)
                
                # Save re-encrypted data
                with open(secret_file, "wb") as f:
                    f.write(new_encrypted_data)
