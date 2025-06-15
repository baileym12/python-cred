import json
import os
from datetime import datetime
from typing import Dict, Optional, List
from pathlib import Path
from .crypto import CryptoManager

class Secret:
    def __init__(
        self,
        name: str,
        value: str,
        secret_type: str,
        environment: str = "default",
        rotation_policy: Optional[Dict] = None,
        metadata: Optional[Dict] = None
    ):
        self.name = name
        self.value = value
        self.secret_type = secret_type
        self.environment = environment
        self.rotation_policy = rotation_policy or {}
        self.metadata = metadata or {}
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at
        self.last_rotated = None

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "secret_type": self.secret_type,
            "environment": self.environment,
            "rotation_policy": self.rotation_policy,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_rotated": self.last_rotated.isoformat() if self.last_rotated else None
        }

    @classmethod
    def from_dict(cls, data: Dict, value: str) -> 'Secret':
        secret = cls(
            name=data["name"],
            value=value,
            secret_type=data["secret_type"],
            environment=data["environment"],
            rotation_policy=data.get("rotation_policy"),
            metadata=data.get("metadata")
        )
        secret.created_at = datetime.fromisoformat(data["created_at"])
        secret.updated_at = datetime.fromisoformat(data["updated_at"])
        if data.get("last_rotated"):
            secret.last_rotated = datetime.fromisoformat(data["last_rotated"])
        return secret

class SecretStorage:
    def __init__(self, storage_path: str = ".secrets"):
        self.storage_path = Path(storage_path)
        self.crypto = CryptoManager()
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        """Ensure the storage directory exists."""
        self.storage_path.mkdir(parents=True, exist_ok=True)
        (self.storage_path / "metadata").mkdir(exist_ok=True)
        (self.storage_path / "secrets").mkdir(exist_ok=True)

    def _get_metadata_path(self, name: str) -> Path:
        """Get the path for a secret's metadata file."""
        return self.storage_path / "metadata" / f"{name}.json"

    def _get_secret_path(self, name: str) -> Path:
        """Get the path for a secret's encrypted value file."""
        return self.storage_path / "secrets" / f"{name}.enc"

    def store(self, secret: Secret) -> None:
        """Store a secret securely."""
        # Encrypt the secret value
        encrypted_data = self.crypto.encrypt(secret.value)
        
        # Store the encrypted value
        secret_path = self._get_secret_path(secret.name)
        with open(secret_path, "wb") as f:
            f.write(encrypted_data)

        # Store the metadata
        metadata_path = self._get_metadata_path(secret.name)
        with open(metadata_path, "w") as f:
            json.dump(secret.to_dict(), f, indent=2)

    def retrieve(self, name: str) -> Optional[Secret]:
        """Retrieve a secret by name."""
        secret_path = self._get_secret_path(name)
        metadata_path = self._get_metadata_path(name)

        if not secret_path.exists() or not metadata_path.exists():
            return None

        # Read the encrypted value
        with open(secret_path, "rb") as f:
            encrypted_data = f.read()
            value = self.crypto.decrypt(encrypted_data)

        # Read the metadata
        with open(metadata_path, "r") as f:
            metadata = json.load(f)

        return Secret.from_dict(metadata, value)

    def list_secrets(self) -> List[Dict]:
        """List all stored secrets (metadata only, no values)."""
        secrets = []
        for metadata_file in (self.storage_path / "metadata").glob("*.json"):
            with open(metadata_file, "r") as f:
                secrets.append(json.load(f))
        return secrets

    def delete(self, name: str) -> bool:
        """Delete a secret."""
        secret_path = self._get_secret_path(name)
        metadata_path = self._get_metadata_path(name)

        if not secret_path.exists() or not metadata_path.exists():
            return False

        secret_path.unlink()
        metadata_path.unlink()
        return True

    def rotate(self, name: str, new_value: str) -> bool:
        """Rotate a secret's value."""
        secret = self.retrieve(name)
        if not secret:
            return False

        secret.value = new_value
        secret.updated_at = datetime.utcnow()
        secret.last_rotated = datetime.utcnow()
        self.store(secret)
        return True 