from pathlib import Path

from database.create_database import create_full_database


def create_env():
    env_path = Path(".env")

    # Перевірка, чи існує файл
    if not env_path.exists():
        # Якщо немає — створити файл з базовим вмістом (або порожній)
        env_path.write_text("# .env файл створено автоматично\n")
        print(".env файл створено")
    else:
        print(".env файл вже існує")


def create_db():
    db_path = Path("tracker.db")
    if not db_path.exists():
        create_full_database()
