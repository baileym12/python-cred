import json
from pathlib import Path
from datetime import datetime

class Secret:
    def __init__(self, name, value, secret_type, environment="default"):
        self.name = name
        self.value = value
        self.secret_type = secret_type
        self.environment = environment
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

    def to_dict(self):
        return {
            "name": self.name,
            "secret_type": self.secret_type,
            "environment": self.environment,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class SecretStorage:
    def __init__(self, storage_path=".secrets"):
        self.storage_path = Path(storage_path)
        self._ensure_storage()

    def _ensure_storage(self):
        self.storage_path.mkdir(parents=True, exist_ok=True)
        (self.storage_path / "metadata").mkdir(exist_ok=True)
        (self.storage_path / "secrets").mkdir(exist_ok=True)

    def store(self, secret):
        metadata_path = self.storage_path / "metadata" / f"{secret.name}.json"
        with open(metadata_path, "w") as f:
            json.dump(secret.to_dict(), f, indent=2)
