from datetime import datetime
from typing import Any

import flet as ft
from flet_route import Basket, Params

from expenses import Expense


class ExpColors:
    DARK_GREEN = "#5D8736"
    GREEN = "#809D3C"
    LIGHT_GREEN = "#A9C46C"
    LIGHT_YELLOW = "#F4FFC3"
    SUPER_DARK_GREEN = "#0c3c0f"
    WHITE = "#FFFFFF"


def expense_view(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    page.title = "Фінансовий трекер"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ExpColors.GREEN,
            on_primary=ExpColors.LIGHT_YELLOW,
            surface=ExpColors.DARK_GREEN,
            on_surface=ExpColors.LIGHT_YELLOW,
        )
    )

    categories = Expense.list_of_categories()
    selected_date = datetime.now()

    def add_category_click(e: Any):
        if new_category_input.value:
            Expense.add_category(new_category_input.value)
            category_dropdown.options.append(ft.dropdown.Option(new_category_input.value))
            category_dropdown.value = new_category_input.value
            new_category_input.value = ""
            new_category_input.visible = False
            page.update()

    def toggle_new_category(e):
        new_category_input.visible = not new_category_input.visible
        page.update()

    def add_expense_click(e: Any):
        if category_dropdown.value and expense_input.value:
            Expense.add_expense(category_dropdown.value, float(expense_input.value), selected_date.strftime("%d/%m/%Y"))
            expense_input.value = ""
            expense_list.controls = build_expense_rows()
            page.update()

    expense_input = ft.TextField(
        label="Сума витрати",
        keyboard_type=ft.KeyboardType.NUMBER,
        prefix_text="₴",
        width=200,
        border_color=ExpColors.LIGHT_YELLOW,
        focused_border_color=ExpColors.LIGHT_GREEN,
        color=ExpColors.LIGHT_YELLOW,
        cursor_color=ExpColors.LIGHT_YELLOW,
        label_style=ft.TextStyle(color=ExpColors.LIGHT_YELLOW),
    )

    new_category_input = ft.TextField(
        label="Нова категорія",
        width=200,
        visible=False,
        border_color=ExpColors.LIGHT_YELLOW,
        focused_border_color=ExpColors.LIGHT_GREEN,
        color=ExpColors.LIGHT_YELLOW,
        cursor_color=ExpColors.LIGHT_YELLOW,
        label_style=ft.TextStyle(color=ExpColors.LIGHT_YELLOW),
    )

    category_dropdown = ft.Dropdown(
        label="Категорія",
        width=200,
        options=[ft.dropdown.Option(c) for c in categories],
        border_color=ExpColors.LIGHT_YELLOW,
        focused_border_color=ExpColors.LIGHT_GREEN,
        color=ExpColors.LIGHT_YELLOW,
        label_style=ft.TextStyle(color=ExpColors.LIGHT_YELLOW),
    )

    add_category_button = ft.IconButton(
        icon=ft.icons.ADD,
        tooltip="Додати нову категорію",
        on_click=toggle_new_category,
        icon_color=ExpColors.LIGHT_YELLOW,
    )

    date_display = ft.Text(f"Дата: {selected_date.strftime('%d/%m/%Y')}", size=16, color=ExpColors.LIGHT_YELLOW)

    add_expense_button = ft.FilledButton(
        "Додати витрату",
        on_click=add_expense_click,
        style=ft.ButtonStyle(bgcolor=ExpColors.SUPER_DARK_GREEN, color=ExpColors.LIGHT_YELLOW),
    )

    def handle_change(e):
        nonlocal selected_date
        if e.control.value:
            selected_date = e.control.value
            date_display.value = f"Дата: {selected_date.strftime('%d/%m/%Y')}"
            page.update()

    def handle_dismissal(e):
        pass

    date_icon_button = ft.ElevatedButton(
        "Обрати дату",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(
            ft.DatePicker(
                first_date=datetime(year=2020, month=10, day=1),
                last_date=datetime.today(),
                on_change=handle_change,
                on_dismiss=handle_dismissal,
            )
        ),
        style=ft.ButtonStyle(bgcolor=ExpColors.SUPER_DARK_GREEN, color=ExpColors.LIGHT_YELLOW),
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
                            ft.Text(
                                f"{expense['category']} - {expense['amount']:.2f} ₴",
                                size=16,
                                color=ExpColors.LIGHT_YELLOW,
                            ),
                            ft.Text(
                                f"Дата: {expense['date'].strftime('%Y-%m-%d')}", size=14, color=ExpColors.LIGHT_GREEN
                            ),
                            ft.Divider(color=ExpColors.LIGHT_GREEN, height=1),
                        ],
                        expand=True,
                    ),
                    ft.IconButton(icon=ft.icons.EDIT, tooltip="Редагувати", icon_color=ExpColors.LIGHT_YELLOW),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        tooltip="Видалити",
                        on_click=lambda e, id=expense["expense_id"]: delete_expense(id),
                        icon_color=ExpColors.LIGHT_YELLOW,
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
            ft.PieChartSection(
                value=40,
                title="Їжа",
                color=ExpColors.LIGHT_GREEN,
                radius=100,
                title_style=ft.TextStyle(color=ExpColors.SUPER_DARK_GREEN, size=12),
            ),
            ft.PieChartSection(
                value=25,
                title="Транспорт",
                color=ExpColors.GREEN,
                radius=100,
                title_style=ft.TextStyle(color=ExpColors.LIGHT_YELLOW, size=12),
            ),
            ft.PieChartSection(
                value=15,
                title="Розваги",
                color=ExpColors.DARK_GREEN,
                radius=100,
                title_style=ft.TextStyle(color=ExpColors.LIGHT_YELLOW, size=12),
            ),
            ft.PieChartSection(
                value=20,
                title="Інше",
                color=ExpColors.SUPER_DARK_GREEN,
                radius=100,
                title_style=ft.TextStyle(color=ExpColors.LIGHT_YELLOW, size=12),
            ),
        ],
        expand=True,
    )

    add_expense_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Додати нову витрату", size=20, weight="bold", color=ExpColors.LIGHT_YELLOW),
                expense_input,
                ft.Row([category_dropdown, add_category_button]),
                new_category_input,
                ft.Row([date_display, date_icon_button]),
                add_expense_button,
            ],
            spacing=10,
        ),
        padding=20,
        border=ft.border.all(1, ExpColors.LIGHT_GREEN),
        border_radius=10,
        margin=10,
        bgcolor=ExpColors.DARK_GREEN,
    )

    expense_list = ft.ListView(spacing=10, padding=20, auto_scroll=True, expand=True)
    expense_list.controls = build_expense_rows()

    expenses_history_container = ft.Container(
        content=ft.Column(
            [ft.Text("Історія витрат", size=20, weight="bold", color=ExpColors.LIGHT_YELLOW), expense_list],
            spacing=10,
            expand=True,
        ),
        expand=True,
        padding=20,
        border=ft.border.all(1, ExpColors.LIGHT_GREEN),
        border_radius=10,
        margin=10,
        bgcolor=ExpColors.DARK_GREEN,
    )

    summary_dialog = ft.AlertDialog(
        title=ft.Text("Підсумки витрат", color=ExpColors.LIGHT_YELLOW),
        content=ft.Column([
            ft.Text("Загальна сума витрат: 450.00 ₴", size=18, weight="bold", color=ExpColors.LIGHT_YELLOW),
            ft.Divider(color=ExpColors.LIGHT_GREEN),
            ft.Text("Витрати по категоріях:", size=16, color=ExpColors.LIGHT_YELLOW),
            ft.Text("Їжа: 250.00 ₴ (55.6%)", color=ExpColors.LIGHT_GREEN),
            ft.Text("Транспорт: 120.00 ₴ (26.7%)", color=ExpColors.LIGHT_GREEN),
            ft.Text("Розваги: 80.00 ₴ (17.8%)", color=ExpColors.LIGHT_GREEN),
            ft.Divider(color=ExpColors.LIGHT_GREEN),
            ft.Text("Витрати за останній тиждень: 300.00 ₴", size=16, color=ExpColors.LIGHT_YELLOW),
        ]),
        actions=[ft.TextButton("Закрити", style=ft.ButtonStyle(color=ExpColors.LIGHT_YELLOW))],
        bgcolor=ExpColors.DARK_GREEN,
    )

    profile_dialog = ft.AlertDialog(
        title=ft.Text("Профіль користувача", color=ExpColors.LIGHT_YELLOW),
        content=ft.Column(
            [
                ft.TextField(
                    label="Ваше ім'я",
                    value="Користувач",
                    border_color=ExpColors.LIGHT_YELLOW,
                    focused_border_color=ExpColors.LIGHT_GREEN,
                    color=ExpColors.LIGHT_YELLOW,
                    cursor_color=ExpColors.LIGHT_YELLOW,
                    label_style=ft.TextStyle(color=ExpColors.LIGHT_YELLOW),
                ),
                ft.TextField(
                    label="Місячний бюджет",
                    keyboard_type=ft.KeyboardType.NUMBER,
                    prefix_text="₴",
                    value="10000",
                    border_color=ExpColors.LIGHT_YELLOW,
                    focused_border_color=ExpColors.LIGHT_GREEN,
                    color=ExpColors.LIGHT_YELLOW,
                    cursor_color=ExpColors.LIGHT_YELLOW,
                    label_style=ft.TextStyle(color=ExpColors.LIGHT_YELLOW),
                ),
                ft.FilledButton(
                    "Зберегти налаштування", style=ft.ButtonStyle(bgcolor=ExpColors.GREEN, color=ExpColors.LIGHT_YELLOW)
                ),
            ],
            spacing=10,
        ),
        actions=[ft.TextButton("Закрити", style=ft.ButtonStyle(color=ExpColors.LIGHT_YELLOW))],
        bgcolor=ExpColors.DARK_GREEN,
    )

    app_bar = ft.AppBar(
        title=ft.Text("Фінансовий трекер", color=ExpColors.LIGHT_YELLOW),
        center_title=True,
        bgcolor=ExpColors.SUPER_DARK_GREEN,
        actions=[
            ft.IconButton(
                icon=ft.icons.SUMMARIZE,
                tooltip="Підсумки витрат",
                on_click=lambda _: page.show_dialog(summary_dialog),
                icon_color=ExpColors.LIGHT_YELLOW,
            ),
            ft.IconButton(
                icon=ft.icons.PERSON,
                tooltip="Профіль",
                on_click=lambda _: page.show_dialog(profile_dialog),
                icon_color=ExpColors.LIGHT_YELLOW,
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
                        [
                            ft.Text(
                                "Розподіл витрат по категоріях", size=20, weight="bold", color=ExpColors.LIGHT_YELLOW
                            ),
                            pie_chart,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=20,
                    ),
                    padding=20,
                    expand=True,
                    bgcolor=ExpColors.DARK_GREEN,
                ),
            ),
        ],
        indicator_color=ExpColors.LIGHT_GREEN,
        label_color=ExpColors.LIGHT_YELLOW,
        unselected_label_color=ExpColors.LIGHT_GREEN,
        divider_color=ExpColors.LIGHT_GREEN,
    )

    main_container = ft.Container(
        content=ft.Column([app_bar, tabs], expand=True),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ExpColors.SUPER_DARK_GREEN, ExpColors.DARK_GREEN],
        ),
        expand=True,
    )

    return ft.View(
        route="/expenses",
        controls=[app_bar, tabs],
        vertical_alignment=ft.MainAxisAlignment.START,
        scroll=ft.ScrollMode.AUTO,
    )
