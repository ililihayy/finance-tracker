# Copyright (c) 2025 ililihayy. All rights reserved.

import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key

from log.logger import log

load_dotenv()


def ensure_encryption_key(env_file: str = ".env", key_name: str = "ENCRYPTION_KEY") -> None:
    encryption_key = os.getenv(key_name)

    if not encryption_key:
        encryption_key = Fernet.generate_key().decode()

        set_key(env_file, key_name, encryption_key)

        log.log("INFO", "The encryption key has been created")


def get_encryption_key() -> str:
    load_dotenv()
    ensure_encryption_key()
    encryption_key = os.getenv("ENCRYPTION_KEY")
    if not encryption_key:
        log.log("ERROR", "Failed to get the key to the database.")
        raise ValueError("ENCRYPTION_KEY is not set in the .env")
    return encryption_key
