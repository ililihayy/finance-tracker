# Copyright (c) 2025 ililihayy. All rights reserved.

from cryptography.fernet import Fernet

from .key import get_encryption_key

ENCRYPTION_KEY = get_encryption_key().encode()
cipher = Fernet(ENCRYPTION_KEY)


def encrypt_data(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()


def decrypt_data(encrypted_data: str) -> str:
    return cipher.decrypt(encrypted_data.encode()).decode()
