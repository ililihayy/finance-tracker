# Copyright (c) 2025 ililihayy. All rights reserved.

import sqlite3

from log.logger import log

from .create_database import conn, create_user_categories_table, create_user_expenses_table, cursor
from .exceptions import CategoryAlreadyExistsError, UserAlreadyExistError


class Utils:
    @staticmethod
    def add_user(username: str, email: str, password: str) -> None:
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password),
            )
            conn.commit()
            create_user_expenses_table(username)
            create_user_categories_table(username)
            log.log("INFO", f"Add user '{username}' with email '{email}'")
        except sqlite3.IntegrityError as err:
            log.log("ERROR", f"User '{username}' or email '{email}' already exists")
            raise UserAlreadyExistError(f"User {username} or email {email} already exists") from err  # noqa: TRY003

    @staticmethod
    def add_expense(username: str, category: str, amount: float, expense_date: str) -> None:
        table_name = f"expenses_{username}"
        cursor.execute(
            f"INSERT INTO {table_name} (category, amount, expense_date) VALUES (?, ?, ?)",
            (category, amount, expense_date),
        )
        conn.commit()
        log.log("INFO", f"Add expense {username} - {category} - {amount} - {expense_date}")

    @staticmethod
    def add_user_category(username: str, category_name: str) -> None:
        categories_table = f"categories_{username}"
        cursor.execute(f"SELECT COUNT(*) FROM {categories_table} WHERE name = ?", (category_name,))
        if cursor.fetchone()[0] > 0:
            log.log("ERROR", f"Category '{category_name}' exists")
            raise CategoryAlreadyExistsError(f"Category '{category_name}' exists")  # noqa: TRY003

        cursor.execute(f"INSERT INTO {categories_table} (name) VALUES (?)", (category_name,))
        conn.commit()
        log.log("INFO", f"Add category for {username} - {category_name}")

    @staticmethod
    def clear_table(username: str, *, expenses: bool = True, categories: bool = True) -> None:
        expenses_table = f"expenses_{username}"
        categories_table = f"categories_{username}"

        if expenses:
            cursor.execute(f"DELETE FROM {expenses_table}")
            log.log("INFO", f"Clear table expenses for {username} ")
        if categories:
            cursor.execute(f"DELETE FROM {categories_table}")
            log.log("INFO", f"Clear table categories for {username} ")

        conn.commit()

    @staticmethod
    def delete_user(username: str) -> None:
        expenses_table = f"expenses_{username}"
        categories_table = f"categories_{username}"

        cursor.execute(f"DROP TABLE IF EXISTS {expenses_table}")
        cursor.execute(f"DROP TABLE IF EXISTS {categories_table}")

        cursor.execute("DELETE FROM users WHERE username = ?", (username,))

        conn.commit()
        log.log("INFO", f"Delete user '{username}'")
