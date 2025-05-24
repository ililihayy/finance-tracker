# Copyright (c) 2025 ililihayy. All rights reserved.

import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from dotenv import load_dotenv, set_key

from log.logger import log

# load_dotenv()
ITERATIONS = 10


def generate_salt_bytes(length: int = 16) -> bytes:
    return os.urandom(length)


def _generate_decryption_key(username: str):
    from database.utils import Utils

    user_id = Utils.get_user_id(username)
    salt = Utils.get_user_salt(username)

    if not user_id or not salt:
        raise ValueError("User ID та сіль повинні бути встановлені перед генерацією ключа")

    user_material = str(user_id).encode("utf-8")

    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITERATIONS, backend=default_backend())

    key = kdf.derive(user_material)
    return base64.urlsafe_b64encode(key)


def ensure_user_encryption_key(username: str, env_file: str = ".env") -> None:
    load_dotenv()
    key_name = f"ENCRYPTION_KEY_{username}"
    encryption_key = os.getenv(key_name)

    if encryption_key is None:
        gen_key = _generate_decryption_key(username)
        encryptor = Fernet(gen_key)
        user_encryption_key = Fernet.generate_key()  # bytes
        encrypted_user_key = encryptor.encrypt(user_encryption_key)
        set_key(env_file, key_name, encrypted_user_key.decode())
        log.log("INFO", "The encryption user`s key has been created")
        return encrypted_user_key.decode()


def get_user_encryption_key(username: str, env_file: str = ".env") -> bytes:
    load_dotenv()
    key_name = f"ENCRYPTION_KEY_{username}"
    encrypted_key = os.getenv(key_name)

    if not encrypted_key:
        encrypted_key = ensure_user_encryption_key(username)
        log.log("ERROR", "Encryption user key not found in environment.")

    decryption_key = _generate_decryption_key(username)
    decryptor = Fernet(decryption_key)
    decrypted_key = decryptor.decrypt(encrypted_key.encode())

    return decrypted_key
