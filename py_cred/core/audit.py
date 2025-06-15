import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class AuditLogger:
    def __init__(self, log_path: str = ".audit_log"):
        self.log_path = Path(log_path)
        self._ensure_log_file()

    def _ensure_log_file(self) -> None:
        """Ensure the audit log file exists."""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self.log_path.touch()

    def log(self, action: str, target: str, details: str) -> None:
        """Log an audit event."""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "target": target,
            "details": details
        }
        
        with open(self.log_path, "a") as f:
            f.write(json.dumps(event) + "\n")

    def get_logs(self, limit: Optional[int] = None) -> List[Dict]:
        """Retrieve audit logs."""
        if not self.log_path.exists():
            return []

        logs = []
        with open(self.log_path, "r") as f:
            for line in f:
                if line.strip():
                    logs.append(json.loads(line))

        if limit:
            logs = logs[-limit:]

        return logs

    def clear_logs(self) -> None:
        """Clear all audit logs."""
        if self.log_path.exists():
            self.log_path.unlink()
        self._ensure_log_file()

    def log_secret_created(self, name, secret_type, environment):
        self.log("secret_created", name, {
            "secret_type": secret_type,
            "environment": environment
        })

    def log_secret_accessed(self, name, environment):
        self.log("secret_accessed", name, {
            "environment": environment
        })
