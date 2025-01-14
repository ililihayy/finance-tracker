# Copyright (c) 2025 ililihayy. All rights reserved.

import sqlite3

conn = sqlite3.connect("tracker.db")
cursor = conn.cursor()


def create_full_database() -> None:
    create_users_table()


def create_user_expenses_table(username: str) -> None:
    table_name = f"expenses_{username}"
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            expense_date DATETIME NOT NULL,
            FOREIGN KEY (category) REFERENCES categories (name)
        )
        """
    )


def create_users_table() -> None:
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL
    )
    """
    )


def create_user_categories_table(username: str) -> None:
    table_name = f"categories_{username}"
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    insert_user_default_categories(username)


def insert_user_default_categories(username: str) -> None:
    categories_table = f"categories_{username}"
    categories = [
        "Food",
        "Health",
        "Transport",
        "Home",
        "Entertainment",
        "Clothes",
        "Secret expenses",
    ]
    for category in categories:
        cursor.execute(f"INSERT OR IGNORE INTO {categories_table} (name) VALUES (?)", (category,))
