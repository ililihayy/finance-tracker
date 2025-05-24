from pathlib import Path
from dotenv import load_dotenv, set_key
from database.create_database import create_users_table


def create_env():
    env_path = Path(".env")

    if not env_path.exists():
        env_path.write_text("")
        print(".env файл створено")
    else:
        print(".env файл вже існує")


def create_db():
    db_path = Path("tracker.db")
    if not db_path.exists():
        create_users_table()
