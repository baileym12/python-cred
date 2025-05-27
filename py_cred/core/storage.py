import json
from pathlib import Path

class SecretStorage:
    def __init__(self):
        self.storage_path = Path(".secrets")
