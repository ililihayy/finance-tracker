# Copyright (c) 2025 ililihayy. All rights reserved.

import sqlite3
from datetime import datetime
from typing import Any

from log.logger import log
from security.utils import decrypt_data, encrypt_data

from .create_database import create_user_categories_table, create_user_expenses_table
from .exceptions import CategoryAlreadyExistsError, UserAlreadyExistError


class Utils:
    @staticmethod
    def add_user(username: str, email: str, password: str) -> None:
        encrypted_email = encrypt_data(email)
        encrypted_password = encrypt_data(password)

        try:
            with sqlite3.connect("tracker.db", check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (username, encrypted_email, encrypted_password),
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

        with sqlite3.connect("tracker.db", check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"INSERT INTO {table_name} (category, amount, expense_date) VALUES (?, ?, ?)",
                (category, encrypted_amount, encrypted_date),
            )
            conn.commit()
        log.log("INFO", f"Add expense {username} - {category} - {encrypted_amount} - {encrypted_date}")

    @staticmethod
    def add_user_category(username: str, category_name: str) -> None:
        categories_table = f"categories_{username}"
        with sqlite3.connect("tracker.db", check_same_thread=False) as conn:
            cursor = conn.cursor()
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

        with sqlite3.connect("tracker.db", check_same_thread=False) as conn:
            cursor = conn.cursor()
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

        with sqlite3.connect("tracker.db", check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {expenses_table}")
            cursor.execute(f"DROP TABLE IF EXISTS {categories_table}")
            cursor.execute("DELETE FROM users WHERE username = ?", (username,))
            conn.commit()
        log.log("INFO", f"Delete user '{username}'")

    @staticmethod
    def get_user_email(username: str) -> str:
        with sqlite3.connect("tracker.db", check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE username = ?", (username,))
            encrypted_email = cursor.fetchone()[0]
        return decrypt_data(encrypted_email)

    @staticmethod
    def get_user_name(password: str) -> str:
        with sqlite3.connect("tracker.db", check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE password = ?", (encrypt_data(password),))
            result = cursor.fetchone()
        return result[0] if result else None

    @staticmethod
    def get_user_password(identifier: str) -> str:
        with sqlite3.connect("tracker.db", check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT password FROM users WHERE username = ? or email = ?", (identifier, encrypt_data(identifier))
            )
            result = cursor.fetchone()
        return decrypt_data(result[0]) if result else None

    @staticmethod
    def get_monthly_expenses_by_category(username: str, category: str, month: str, year: str) -> float:
        table_name = f"expenses_{username}"
        with sqlite3.connect("tracker.db", check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                SELECT amount FROM {table_name}
                WHERE category = ?
                AND strftime('%m', expense_date) = ?
                AND strftime('%Y', expense_date) = ?
                """,
                (category, month, year),
            )
            expenses = cursor.fetchall()
        total = sum(float(decrypt_data(expense[0])) for expense in expenses)
        log.log("INFO", f"Total expenses for {username} in category '{category}' in {month}/{year}: {total}")
        return total

    @staticmethod
    def get_monthly_expenses(username: str, month: str, year: str) -> float:
        table_name = f"expenses_{username}"
        with sqlite3.connect("tracker.db", check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                SELECT amount FROM {table_name}
                WHERE strftime('%m', expense_date) = ?
                AND strftime('%Y', expense_date) = ?
                """,
                (month, year),
            )
            expenses = cursor.fetchall()
        total = sum(float(decrypt_data(expense[0])) for expense in expenses)
        log.log("INFO", f"Total expenses for {username} in {month}/{year}: {total}")
        return total

    @staticmethod
    def get_user_categories(username: str) -> list[str]:
        categories_table = f"categories_{username}"
        with sqlite3.connect("tracker.db", check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT name FROM {categories_table}")
            categories = cursor.fetchall()
        result = [category[0] for category in categories]
        log.log("INFO", f"Fetched categories for user '{username}': {result}")
        return result

    @staticmethod
    def get_user_expenses(username: str) -> list[dict[str, Any]]:
        table_name = f"expenses_{username}"
        with sqlite3.connect("tracker.db", check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT expense_id, amount, category, expense_date FROM {table_name}
                ORDER BY expense_date DESC
            """)
            rows = cursor.fetchall()

        expenses = []
        for expense_id, amount, category, date_str in rows:
            date = datetime.strptime(decrypt_data(date_str), "%d/%m/%Y")
            expenses.append({
                "expense_id": expense_id,
                "amount": float(decrypt_data(amount)),
                "category": category,
                "date": date,
            })

        return expenses

    @staticmethod
    def delete_user_expense(username: str, expense_id: int):
        table_name = f"expenses_{username}"
        with sqlite3.connect("tracker.db", check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table_name} WHERE expense_id = ?", (expense_id,))
            conn.commit()

    @staticmethod
    def update_user_expense(username: str, expense_id: int, category: str, amount: float, date: str):
        table_name = f"expenses_{username}"
        with sqlite3.connect("tracker.db", check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                UPDATE {table_name}
                SET category = ?, amount = ?, expense_date = ?
                WHERE expense_id = ?
                """,
                (category, str(amount), date, expense_id),
            )
            conn.commit()
