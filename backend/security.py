import os
import hashlib
import magic
import re
from pathlib import Path
from cryptography.fernet import Fernet

class SecurityManager:
    def __init__(self):
        # Retrieve key from environment variable, or generate a stable default for development
        key = os.environ.get("ENCRYPTION_KEY")
        if not key:
            # Generate a new key if it doesn't exist
            key = Fernet.generate_key().decode()
            os.environ["ENCRYPTION_KEY"] = key
        self.cipher = Fernet(key.encode())
    
    def validate_file(self, file_content: bytes, filename: str) -> tuple[bool, str]:
        """Check if file is safe to process"""
        
        # 1. Check file size (50MB limit)
        if len(file_content) > 50 * 1024 * 1024:
            return False, "File too large (max 50MB)"
        
        # 2. Check MIME type (not just extension!) using magic bytes
        mime = magic.from_buffer(file_content, mime=True)
        allowed_mimes = ['application/pdf', 'image/jpeg', 'image/png', 'text/plain']
        
        if mime not in allowed_mimes:
            return False, f"Invalid file type: {mime}"
        
        # 3. Sanitize filename (prevent path traversal / directory injection)
        safe_name = hashlib.sha256(filename.encode()).hexdigest()
        safe_name += Path(filename).suffix
        
        return True, safe_name
    
    def encrypt_file(self, file_path: str):
        """Encrypt file at rest"""
        with open(file_path, 'rb') as f:
            encrypted = self.cipher.encrypt(f.read())
        
        with open(file_path + '.enc', 'wb') as f:
            f.write(encrypted)
        
        # Remove original unencrypted file
        Path(file_path).unlink()
        
    def decrypt_file(self, encrypted_file_path: str) -> bytes:
        """Decrypt file back to bytes"""
        with open(encrypted_file_path, 'rb') as f:
            decrypted = self.cipher.decrypt(f.read())
        return decrypted
    
    def sanitize_text(self, text: str) -> str:
        """Remove potential injection attacks"""
        # Remove any script tags
        text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.DOTALL)
        # Remove SQL query strings patterns
        text = re.sub(r'--|;|DROP|SELECT|INSERT', '', text, flags=re.IGNORECASE)
        return text
