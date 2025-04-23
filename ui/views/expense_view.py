from datetime import datetime
from typing import Any

import flet as ft  # type: ignore[import-not-found]
from flet_route import Basket, Params  # type: ignore[import-not-found]

from expenses import Expense


def expense_view(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    page.title = "Фінансовий трекер"
    page.theme_mode = ft.ThemeMode.SYSTEM

    categories = Expense.list_of_categories()
    selected_date = datetime.now()

    def add_category_click(e: Any):
        Expense.add_category(new_category_input.value)

    def add_expense_click(e: Any):
        Expense.add_expense(category_dropdown.value, float(expense_input.value), selected_date.strftime("%d/%m/%Y"))
        print("add expense")

        expense_list.controls = build_expense_rows()
        expense_list.update()

    expense_input = ft.TextField(label="Сума витрати", keyboard_type=ft.KeyboardType.NUMBER, prefix_text="₴", width=200)
    new_category_input = ft.TextField(label="Нова категорія", width=200, visible=False)
    category_dropdown = ft.Dropdown(label="Категорія", width=200, options=[ft.dropdown.Option(c) for c in categories])
    add_category_button = ft.IconButton(icon=ft.icons.ADD, tooltip="Додати нову категорію", on_click=add_category_click)
    date_display = ft.Text(f"Дата: {selected_date.strftime('%d/%m/%Y')}", size=16)
    add_expense_button = ft.FilledButton("Додати витрату", on_click=add_expense_click)

    # Date select

    def handle_change(e):
        nonlocal selected_date
        if e.control.value:
            selected_date = e.control.value
            date_display.value = f"Дата: {selected_date.strftime('%d/%m/%Y')}"
            page.update()

    def handle_dismissal(e):
        page.add(ft.Text("DatePicker dismissed"))

    date_icon_button = ft.ElevatedButton(
        "Pick date",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(
            ft.DatePicker(
                first_date=datetime(year=2020, month=10, day=1),
                last_date=datetime.today(),
                on_change=handle_change,
                on_dismiss=handle_dismissal,
            )
        ),
    )

    def delete_expense(expense_id: int):
        Expense.delete_expense(expense_id)
        expense_list.controls = build_expense_rows()
        expense_list.update()

    def build_expense_rows():
        db_expenses = Expense.get_all_user_expenses()
        db_expenses.sort(key=lambda x: x["date"], reverse=True)
        rows = []

        for expense in db_expenses:
            row = ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(f"{expense['category']} - {expense['amount']:.2f} ₴", size=16),
                            ft.Text(f"Дата: {expense['date'].strftime('%Y-%m-%d')}", size=14),
                            ft.Text("______________________________________________________________"),
                        ],
                        expand=True,
                    ),
                    ft.IconButton(icon=ft.icons.EDIT, tooltip="Редагувати"),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        tooltip="Видалити",
                        on_click=lambda e, id=expense["expense_id"]: delete_expense(id),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            rows.append(row)

        return rows

    pie_chart = ft.PieChart(
        width=400,
        height=400,
        sections=[
            ft.PieChartSection(value=40, title="Їжа", color=ft.colors.BLUE),
            ft.PieChartSection(value=25, title="Транспорт", color=ft.colors.GREEN),
            ft.PieChartSection(value=15, title="Розваги", color=ft.colors.ORANGE),
            ft.PieChartSection(value=20, title="Інше", color=ft.colors.GREY),
        ],
        expand=True,
    )

    add_expense_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Додати нову витрату", size=20, weight="bold"),
                expense_input,
                ft.Row([category_dropdown, add_category_button]),
                new_category_input,
                ft.Row([date_display, date_icon_button]),
                add_expense_button,
            ],
            spacing=10,
        ),
        padding=20,
        border=ft.border.all(1, ft.colors.OUTLINE),
        border_radius=10,
        margin=10,
    )

    expense_list = ft.ListView(spacing=10, padding=20, auto_scroll=True, expand=True)
    expense_list.controls = build_expense_rows()

    expenses_history_container = ft.Container(
        content=ft.Column([ft.Text("Історія витрат", size=20, weight="bold"), expense_list], spacing=10, expand=True),
        expand=True,
        padding=20,
        border=ft.border.all(1, ft.colors.OUTLINE),
        border_radius=10,
        margin=10,
    )

    summary_dialog = ft.AlertDialog(
        title=ft.Text("Підсумки витрат"),
        content=ft.Column([
            ft.Text("Загальна сума витрат: 450.00 ₴", size=18, weight="bold"),
            ft.Divider(),
            ft.Text("Витрати по категоріях:", size=16),
            ft.Text("Їжа: 250.00 ₴ (55.6%)"),
            ft.Text("Транспорт: 120.00 ₴ (26.7%)"),
            ft.Text("Розваги: 80.00 ₴ (17.8%)"),
            ft.Divider(),
            ft.Text("Витрати за останній тиждень: 300.00 ₴", size=16),
        ]),
        actions=[ft.TextButton("Закрити")],
    )

    profile_dialog = ft.AlertDialog(
        title=ft.Text("Профіль користувача"),
        content=ft.Column(
            [
                ft.TextField(label="Ваше ім'я", value="Користувач"),
                ft.TextField(
                    label="Місячний бюджет", keyboard_type=ft.KeyboardType.NUMBER, prefix_text="₴", value="10000"
                ),
                ft.FilledButton("Зберегти налаштування"),
            ],
            spacing=10,
        ),
        actions=[ft.TextButton("Закрити")],
    )

    app_bar = ft.AppBar(
        title=ft.Text("Фінансовий трекер"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(
                icon=ft.icons.SUMMARIZE,
                tooltip="Підсумки витрат",
                on_click=lambda _: page.dialogs.append(summary_dialog),
            ),
            ft.IconButton(
                icon=ft.icons.PERSON, tooltip="Профіль", on_click=lambda _: page.dialogs.append(profile_dialog)
            ),
        ],
    )

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Витрати",
                icon=ft.icons.PAID,
                content=ft.Column([add_expense_container, expenses_history_container], spacing=10, expand=True),
            ),
            ft.Tab(
                text="Діаграма",
                icon=ft.icons.PIE_CHART,
                content=ft.Container(
                    content=ft.Column(
                        [ft.Text("Розподіл витрат по категоріях", size=20, weight="bold"), pie_chart],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=20,
                    ),
                    padding=20,
                    expand=True,
                ),
            ),
        ],
    )

    return ft.View(
        route="/expenses",
        controls=[app_bar, tabs],
        vertical_alignment=ft.MainAxisAlignment.START,
        scroll=ft.ScrollMode.AUTO,
    )
