"""
tests/test_crypto.py
"""
import pytest
from models.crypto import get_fernet

def test_crypto_fernet_generation():
    password = "MySuperSecretMasterPassword"
    salt = b"somesecretsalt32byteslongexactly!12"
    
    fernet = get_fernet(password, salt)
    assert fernet is not None
    
def test_crypto_encrypt_decrypt():
    password = "MasterPassword"
    salt = b"12345678901234567890123456789012"
    
    fernet = get_fernet(password, salt)
    
    original_text = "This is a secret message"
    encrypted = fernet.encrypt(original_text.encode())
    
    # Doit être crypté
    assert encrypted != original_text.encode()
    
    # Doit pouvoir être déchiffré
    decrypted = fernet.decrypt(encrypted).decode()
    assert decrypted == original_text
