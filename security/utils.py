# Copyright (c) 2025 ililihayy. All rights reserved.

from cryptography.fernet import Fernet

from auth.auth import Auth
from .key import get_encryption_key
from .user_key import get_user_encryption_key

ENCRYPTION_KEY = get_encryption_key().encode()

cipher = Fernet(ENCRYPTION_KEY)


def encrypt_data(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()


def decrypt_data(encrypted_data: str) -> str:
    return cipher.decrypt(encrypted_data.encode()).decode()


def encrypt_data_user(data: str) -> str:
    ENCRYPTION_KEY_USER = get_user_encryption_key(Auth.current_user)
    cipher_user = Fernet(ENCRYPTION_KEY_USER)
    return cipher_user.encrypt(data.encode()).decode()


def decrypt_data_user(encrypted_data: str) -> str:
    ENCRYPTION_KEY_USER = get_user_encryption_key(Auth.current_user)
    cipher_user = Fernet(ENCRYPTION_KEY_USER)
    return cipher_user.decrypt(encrypted_data.encode()).decode()
