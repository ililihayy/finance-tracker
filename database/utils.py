# Copyright (c) 2025 ililihayy. All rights reserved.

import sqlite3

from .create_database import conn, create_user_categories_table, create_user_expenses_table, cursor
from .exceptions import CategoryAlreadyExistsError, UserAlreadyExistError


class Utils:
    @staticmethod
    def add_user(username: str) -> None:
        try:
            cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
            conn.commit()
            create_user_expenses_table(username)
            create_user_categories_table(username)
        except sqlite3.IntegrityError as err:
            raise UserAlreadyExistError(f"User {username} already exists") from err  # noqa: TRY003

    @staticmethod
    def add_expense(username: str, category: str, amount: float, expense_date: str) -> None:
        table_name = f"expenses_{username}"
        cursor.execute(
            f"INSERT INTO {table_name} (category, amount, expense_date) VALUES (?, ?, ?)",
            (category, amount, expense_date),
        )
        conn.commit()

    @staticmethod
    def add_user_category(username: str, category_name: str) -> None:
        categories_table = f"categories_{username}"
        cursor.execute(f"SELECT COUNT(*) FROM {categories_table} WHERE name = ?", (category_name,))
        if cursor.fetchone()[0] > 0:
            raise CategoryAlreadyExistsError(f"Category '{category_name}' exists")  # noqa: TRY003

        cursor.execute(f"INSERT INTO {categories_table} (name) VALUES (?)", (category_name,))
        conn.commit()

    @staticmethod
    def clear_table(username: str, *, expenses: bool = True, categories: bool = True) -> None:
        expenses_table = f"expenses_{username}"
        categories_table = f"categories_{username}"

        if expenses:
            cursor.execute(f"DELETE FROM {expenses_table}")
        if categories:
            cursor.execute(f"DELETE FROM {categories_table}")

        conn.commit()

    @staticmethod
    def delete_user(username: str) -> None:
        expenses_table = f"expenses_{username}"
        categories_table = f"categories_{username}"

        cursor.execute(f"DROP TABLE IF EXISTS {expenses_table}")
        cursor.execute(f"DROP TABLE IF EXISTS {categories_table}")

        cursor.execute("DELETE FROM users WHERE username = ?", (username,))

        conn.commit()
