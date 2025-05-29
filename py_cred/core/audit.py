import json
from datetime import datetime
from pathlib import Path

class AuditLogger:
    def __init__(self, log_path="audit.log"):
        self.log_path = Path(log_path)
        self._ensure_log_file()

    def _ensure_log_file(self):
        if not self.log_path.exists():
            self.log_path.touch()

    def _log_event(self, event_type, details):
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "details": details
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(event) + "
")

    def log_secret_created(self, name, secret_type, environment):
        self._log_event("secret_created", {
            "name": name,
            "secret_type": secret_type,
            "environment": environment
        })

    def log_secret_accessed(self, name, environment):
        self._log_event("secret_accessed", {
            "name": name,
            "environment": environment
        })
