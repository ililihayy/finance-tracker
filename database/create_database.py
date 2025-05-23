# Copyright (c) 2025 ililihayy. All rights reserved.

import sqlite3

from log.logger import log

path = "tracker.db"  # дефолт на випадок відсутності змінної


def create_full_database() -> None:
    create_users_table()


def create_user_expenses_table(username: str) -> None:
    table_name = f"expenses_{username}"
    with sqlite3.connect(path, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                amount TEXT NOT NULL,
                expense_date TEXT NOT NULL,
                FOREIGN KEY (category) REFERENCES categories_{username} (name)
            )
            """
        )
        conn.commit()
    log.log("INFO", f"Create expenses table for username {username}")
    create_user_categories_table(username)


def create_users_table() -> None:
    with sqlite3.connect(path, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                salt BLOB,
                is_blocked BOOLEAN DEFAULT FALSE
            )
            """
        )
        conn.commit()
    log.log("INFO", "Create users table")


def create_user_categories_table(username: str) -> None:
    table_name = f"categories_{username}"
    with sqlite3.connect(path, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
            """
        )
        conn.commit()
    insert_user_default_categories(username)
    log.log("INFO", f"Create categories table for username {username}")


def insert_user_default_categories(username: str) -> None:
    categories_table = f"categories_{username}"
    categories = ["Харчування", "Здоров'я", "Транспорт", "Дім", "Розваги", "Одяг", "Секретні витрати"]
    with sqlite3.connect(path, check_same_thread=False) as conn:
        cursor = conn.cursor()
        for category in categories:
            cursor.execute(f"INSERT OR IGNORE INTO {categories_table} (name) VALUES (?)", (category,))
        conn.commit()
    log.log("INFO", "Insert default categories")


# if __name__ == "__main__":
#     create_full_database()
