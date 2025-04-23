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
