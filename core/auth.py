"""
KVGroove Authentication
Handles password protection for the app
"""

import hashlib
import json
from pathlib import Path
from typing import Optional


class Auth:
    """Password authentication manager"""
    
    def __init__(self, data_path: str = "data/auth.json"):
        self.data_path = Path(data_path)
        self._password_hash: Optional[str] = None
        self._load()
    
    def _load(self):
        """Load stored password hash"""
        try:
            if self.data_path.exists():
                with open(self.data_path, 'r') as f:
                    data = json.load(f)
                    self._password_hash = data.get('password_hash')
        except Exception:
            self._password_hash = None
    
    def _save(self):
        """Save password hash"""
        try:
            self.data_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.data_path, 'w') as f:
                json.dump({'password_hash': self._password_hash}, f)
        except Exception as e:
            print(f"Error saving auth data: {e}")
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def is_password_set(self) -> bool:
        """Check if a password has been set"""
        return self._password_hash is not None
    
    def set_password(self, password: str):
        """Set a new password"""
        self._password_hash = self._hash_password(password)
        self._save()
    
    def verify_password(self, password: str) -> bool:
        """Verify a password against the stored hash"""
        if not self._password_hash:
            return True  # No password set
        return self._hash_password(password) == self._password_hash
    
    def remove_password(self):
        """Remove password protection"""
        self._password_hash = None
        self._save()
    
    def change_password(self, old_password: str, new_password: str) -> bool:
        """Change password (requires old password verification)"""
        if self.verify_password(old_password):
            self.set_password(new_password)
            return True
        return False
