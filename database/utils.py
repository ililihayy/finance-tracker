# Copyright (c) 2025 ililihayy. All rights reserved.

import sqlite3

from log.logger import log
from security.utils import decrypt_data, encrypt_data

from .create_database import conn, create_user_categories_table, create_user_expenses_table, cursor
from .exceptions import CategoryAlreadyExistsError, UserAlreadyExistError


class Utils:
    @staticmethod
    def add_user(username: str, email: str, password: str) -> None:
        encrypted_email = encrypt_data(email)
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, encrypted_email, encrypt_data(password)),
            )
            conn.commit()
            create_user_expenses_table(username)
            create_user_categories_table(username)
            log.log("INFO", f"Add user '{username}' with email '{encrypted_email}'")
        except sqlite3.IntegrityError as err:
            log.log("ERROR", f"User '{username}' or email '{encrypted_email}' already exists")
            raise UserAlreadyExistError(f"User {username} or email {encrypted_email} already exists") from err

    @staticmethod
    def add_expense(username: str, category: str, amount: float, expense_date: str) -> None:
        table_name = f"expenses_{username}"
        encrypted_amount = encrypt_data(str(amount))
        encrypted_date = encrypt_data(expense_date)

        cursor.execute(
            f"INSERT INTO {table_name} (category, amount, expense_date) VALUES (?, ?, ?)",
            (category, encrypted_amount, encrypted_date),
        )
        conn.commit()
        log.log("INFO", f"Add expense {username} - {category} - {encrypted_amount} - {encrypted_date}")

    @staticmethod
    def add_user_category(username: str, category_name: str) -> None:
        categories_table = f"categories_{username}"
        cursor.execute(f"SELECT COUNT(*) FROM {categories_table} WHERE name = ?", (category_name,))
        if cursor.fetchone()[0] > 0:
            log.log("ERROR", f"Category '{category_name}' exists")
            raise CategoryAlreadyExistsError(f"Category '{category_name}' exists")

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

    @staticmethod
    def get_user_email(username: str) -> str:
        cursor.execute("SELECT email FROM users WHERE username = ?", (username,))
        encrypted_email = cursor.fetchone()[0]
        return decrypt_data(encrypted_email)

    @staticmethod
    def get_user_password(username: str) -> str:
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        encrypted_password = cursor.fetchone()[0]
        return decrypt_data(encrypted_password)
