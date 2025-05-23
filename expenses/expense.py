from datetime import datetime

from auth import Auth
from database import Utils as Db


class Expense:
    @staticmethod
    def list_of_categories() -> list:
        return Db.get_user_categories(Auth.current_user)

    @staticmethod
    def add_category(category: str):
        Db.add_user_category(Auth.current_user, category)

    @staticmethod
    def add_expense(category: str, amount: float, expense_date: str):
        Db.add_expense(Auth.current_user, category, amount, expense_date)

    @staticmethod
    def get_all_user_expenses():
        return Db.get_user_expenses(Auth.current_user)

    @staticmethod
    def delete_expense(id: int):
        Db.delete_user_expense(Auth.current_user, id)

    @staticmethod
    def get_expenses_by_date_range(start_date: datetime, end_date: datetime) -> list[dict]:
        """Get all expenses within a date range."""
        all_expenses = Db.get_user_expenses(Auth.current_user)
        filtered_expenses = [expense for expense in all_expenses if start_date <= expense["date"] <= end_date]
        return filtered_expenses

    @staticmethod
    def update_expense(expense_id: int, category: str, amount: float, expense_date: str):
        """Update an existing expense."""
        Db.update_user_expense(Auth.current_user, expense_id, category, amount, expense_date)
