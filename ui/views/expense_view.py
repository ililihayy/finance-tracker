from calendar import monthrange
from datetime import datetime, timedelta
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

    CHART_COLORS = [
        "#FF6B6B",  # Coral Red
        "#4ECDC4",  # Turquoise
        "#45B7D1",  # Sky Blue
        "#96CEB4",  # Sage Green
        "#FFEEAD",  # Cream Yellow
        "#D4A5A5",  # Dusty Rose
        "#9B59B6",  # Purple
        "#3498DB",  # Blue
        "#E67E22",  # Orange
        "#2ECC71",  # Emerald
        "#F1C40F",  # Yellow
        "#1ABC9C",  # Teal
    ]


class MonthlyStatsView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_date = datetime.now()
        self.current_month = self.current_date.month
        self.current_year = self.current_date.year
        self.color_index = 0
        self.container = None  # Store reference to the container for updates

    def get_next_color(self) -> str:
        color = ExpColors.CHART_COLORS[self.color_index]
        self.color_index = (self.color_index + 1) % len(ExpColors.CHART_COLORS)
        return color

    def get_monthly_expenses(self) -> dict[str, float]:
        start_date = datetime(self.current_year, self.current_month, 1)
        _, last_day = monthrange(self.current_year, self.current_month)
        end_date = datetime(self.current_year, self.current_month, last_day)

        expenses = Expense.get_expenses_by_date_range(start_date, end_date)
        category_totals = {}

        # Only add categories that have expenses
        for expense in expenses:
            category = expense["category"]
            amount = float(expense["amount"])
            if amount > 0:  # Only include categories with expenses
                category_totals[category] = category_totals.get(category, 0) + amount

        return category_totals

    def update_view(self):
        """Update the monthly view with current data"""
        if self.container:
            self.container.content = self.build_monthly_content()
            self.page.update()

    def build_monthly_content(self) -> ft.Column:
        expenses = self.get_monthly_expenses()
        total_amount = sum(expenses.values())

        # Reset color index for new chart
        self.color_index = 0

        # Create pie chart sections only for categories with expenses
        sections = []
        for category, amount in expenses.items():
            if amount > 0:  # Only add sections for categories with expenses
                percentage = (amount / total_amount * 100) if total_amount > 0 else 0
                sections.append(
                    ft.PieChartSection(
                        value=percentage,
                        title=category,
                        color=self.get_next_color(),
                        radius=100,
                        title_style=ft.TextStyle(color=ExpColors.SUPER_DARK_GREEN, size=12, weight=ft.FontWeight.BOLD),
                    )
                )

        # Create category summary only for categories with expenses
        self.color_index = 0  # Reset color index for summary

        # Create month navigation buttons
        def change_month(delta: int):
            new_date = datetime(self.current_year, self.current_month, 1) + timedelta(days=32 * delta)
            self.current_month = new_date.month
            self.current_year = new_date.year
            self.current_date = new_date
            self.update_view()

        month_navigation = ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_IOS, on_click=lambda _: change_month(-1), icon_color=ExpColors.LIGHT_YELLOW
                ),
                ft.Text(self.current_date.strftime("%B %Y"), size=20, color=ExpColors.LIGHT_YELLOW),
                ft.IconButton(
                    icon=ft.Icons.ARROW_FORWARD_IOS,
                    on_click=lambda _: change_month(1),
                    icon_color=ExpColors.LIGHT_YELLOW,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Create empty state message if no expenses
        empty_state = (
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(name=ft.Icons.PIE_CHART_OUTLINE, size=64, color=ExpColors.LIGHT_YELLOW),
                        ft.Text(
                            "Немає витрат за цей місяць",
                            size=20,
                            color=ExpColors.LIGHT_YELLOW,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
            if total_amount == 0
            else None
        )

        category_summary = ft.Column(
            [
                ft.Text(f"{self.current_date.strftime('%B %Y')}", size=24, weight="bold", color=ExpColors.LIGHT_YELLOW),
                ft.Text(f"Загальна сума: {total_amount:.2f} ₴", size=18, color=ExpColors.LIGHT_YELLOW),
                ft.Divider(color=ExpColors.LIGHT_GREEN),
            ]
            + [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                width=20,
                                height=20,
                                bgcolor=self.get_next_color(),
                                border_radius=5,
                            ),
                            ft.Text(
                                f"{category}: {amount:.2f} ₴ ({(amount / total_amount * 100 if total_amount > 0 else 0.0):.1f}%)",
                                color=ExpColors.LIGHT_GREEN,
                                size=16,
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=ft.padding.only(left=10, right=10, top=5, bottom=5),
                )
                for category, amount in expenses.items()
                if amount > 0  # Only show categories with expenses
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        return ft.Column(
            [
                month_navigation,
                ft.Row(
                    [
                        ft.Container(
                            content=empty_state or ft.PieChart(sections=sections, width=400, height=400, expand=True),
                            expand=True,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=category_summary,
                            padding=20,
                            border=ft.border.all(1, ExpColors.LIGHT_GREEN),
                            border_radius=10,
                            expand=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    expand=True,
                ),
            ],
            spacing=20,
            expand=True,
        )

    def build_monthly_view(self) -> ft.Container:
        self.container = ft.Container(
            content=self.build_monthly_content(), padding=20, expand=True, bgcolor=ExpColors.DARK_GREEN
        )
        return self.container


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
        category_name = new_category_input.value.strip()
        if not category_name:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Будь ласка, введіть назву категорії"), bgcolor=ExpColors.SUPER_DARK_GREEN
            )
            page.snack_bar.open = True
            page.update()
            return

        if category_name in categories:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Така категорія вже існує"), bgcolor=ExpColors.SUPER_DARK_GREEN
            )
            page.snack_bar.open = True
            page.update()
            return

        try:
            Expense.add_category(category_name)
            categories.append(category_name)
            category_dropdown.options = [ft.dropdown.Option(c) for c in categories]
            category_dropdown.value = category_name
            new_category_input.value = ""
            update_category_visibility(False)
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Категорію '{category_name}' додано успішно"), bgcolor=ExpColors.SUPER_DARK_GREEN
            )
            page.snack_bar.open = True
            page.update()
        except Exception as err:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Помилка при додаванні категорії: {err!s}"), bgcolor=ExpColors.SUPER_DARK_GREEN
            )
            page.snack_bar.open = True
            page.update()

    def toggle_new_category(e):
        new_category_input.visible = not new_category_input.visible
        if new_category_input.visible:
            new_category_input.focus()
        page.update()

    def add_expense_click(e: Any):
        if category_dropdown.value and expense_input.value:
            Expense.add_expense(category_dropdown.value, float(expense_input.value), selected_date.strftime("%d/%m/%Y"))
            expense_input.value = ""
            expense_list.controls = build_expense_rows()
            monthly_stats.update_view()  # Update monthly stats when new expense is added
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
        hint_text="Введіть назву нової категорії",
        hint_style=ft.TextStyle(color=ExpColors.LIGHT_GREEN),
        on_submit=add_category_click,  # Allow adding category by pressing Enter
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
        icon=ft.Icons.ADD,
        tooltip="Додати нову категорію",
        icon_color=ExpColors.LIGHT_YELLOW,
    )

    category_row = ft.Row(
        [
            category_dropdown,
            add_category_button,
            ft.Container(
                content=ft.Column(
                    [
                        new_category_input,
                        ft.ElevatedButton(
                            "Додати категорію",
                            on_click=add_category_click,
                            style=ft.ButtonStyle(bgcolor=ExpColors.SUPER_DARK_GREEN, color=ExpColors.LIGHT_YELLOW),
                            visible=False,
                        ),
                    ],
                    spacing=5,
                ),
                visible=False,
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=10,
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
        icon=ft.Icons.CALENDAR_MONTH,
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
        monthly_stats.update_view()  # Update monthly stats when expense is deleted
        expense_list.update()

    def show_edit_dialog(expense: dict):
        edit_category_dropdown = ft.Dropdown(
            label="Категорія",
            width=200,
            options=[ft.dropdown.Option(c) for c in categories],
            value=expense["category"],
            border_color=ExpColors.LIGHT_YELLOW,
            focused_border_color=ExpColors.LIGHT_GREEN,
            color=ExpColors.LIGHT_YELLOW,
            label_style=ft.TextStyle(color=ExpColors.LIGHT_YELLOW),
        )

        edit_amount_input = ft.TextField(
            label="Сума витрати",
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="₴",
            width=200,
            value=str(expense["amount"]),
            border_color=ExpColors.LIGHT_YELLOW,
            focused_border_color=ExpColors.LIGHT_GREEN,
            color=ExpColors.LIGHT_YELLOW,
            cursor_color=ExpColors.LIGHT_YELLOW,
            label_style=ft.TextStyle(color=ExpColors.LIGHT_YELLOW),
        )

        edit_date = datetime.strptime(expense["date"].strftime("%d/%m/%Y"), "%d/%m/%Y")
        edit_date_display = ft.Text(f"Дата: {edit_date.strftime('%d/%m/%Y')}", size=16, color=ExpColors.LIGHT_YELLOW)

        def handle_edit_date_change(e):
            nonlocal edit_date
            if e.control.value:
                edit_date = e.control.value
                edit_date_display.value = f"Дата: {edit_date.strftime('%d/%m/%Y')}"
                page.update()

        edit_date_button = ft.ElevatedButton(
            "Обрати дату",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: page.open(
                ft.DatePicker(
                    first_date=datetime(year=2020, month=10, day=1),
                    last_date=datetime.today(),
                    on_change=handle_edit_date_change,
                    on_dismiss=lambda _: None,
                )
            ),
            style=ft.ButtonStyle(bgcolor=ExpColors.SUPER_DARK_GREEN, color=ExpColors.LIGHT_YELLOW),
        )

        def save_edit(e):
            if edit_category_dropdown.value and edit_amount_input.value:
                try:
                    amount = float(edit_amount_input.value)
                    Expense.update_expense(
                        expense["expense_id"], edit_category_dropdown.value, amount, edit_date.strftime("%d/%m/%Y")
                    )
                    expense_list.controls = build_expense_rows()
                    monthly_stats.update_view()
                    page.dialog = None  # Close dialog
                    page.update()
                except ValueError:
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text("Будь ласка, введіть коректну суму"), bgcolor=ExpColors.SUPER_DARK_GREEN
                    )
                    page.snack_bar.open = True
                    page.update()

        edit_dialog = ft.AlertDialog(
            title=ft.Text("Редагувати витрату", color=ExpColors.LIGHT_YELLOW),
            content=ft.Column(
                [
                    edit_category_dropdown,
                    edit_amount_input,
                    ft.Row([edit_date_display, edit_date_button]),
                ],
                spacing=20,
            ),
            actions=[
                ft.TextButton(
                    "Скасувати",
                    on_click=lambda _: setattr(page, "dialog", None),
                    style=ft.ButtonStyle(color=ExpColors.LIGHT_YELLOW),
                ),
                ft.FilledButton(
                    "Зберегти",
                    on_click=save_edit,
                    style=ft.ButtonStyle(bgcolor=ExpColors.SUPER_DARK_GREEN, color=ExpColors.LIGHT_YELLOW),
                ),
            ],
            bgcolor=ExpColors.DARK_GREEN,
        )

        page.dialog = edit_dialog
        page.update()

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
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        tooltip="Редагувати",
                        on_click=lambda e, exp=expense: show_edit_dialog(exp),
                        icon_color=ExpColors.LIGHT_YELLOW,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        tooltip="Видалити",
                        on_click=lambda e, id=expense["expense_id"]: delete_expense(id),
                        icon_color=ExpColors.LIGHT_YELLOW,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            rows.append(row)

        return rows

    def update_category_visibility(visible: bool):
        new_category_input.visible = visible
        category_row.controls[2].visible = visible
        if visible:
            new_category_input.focus()
        page.update()

    add_category_button.on_click = lambda e: update_category_visibility(not new_category_input.visible)

    add_expense_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Додати нову витрату", size=20, weight="bold", color=ExpColors.LIGHT_YELLOW),
                expense_input,
                category_row,
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

    app_bar = ft.AppBar(
        title=ft.Text("Фінансовий трекер", color=ExpColors.LIGHT_YELLOW),
        center_title=True,
        bgcolor=ExpColors.SUPER_DARK_GREEN,
    )

    monthly_stats = MonthlyStatsView(page)

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Витрати",
                icon=ft.Icons.PAID,
                content=ft.Column([add_expense_container, expenses_history_container], spacing=10, expand=True),
            ),
            ft.Tab(
                text="Місячна статистика",
                icon=ft.Icons.CALENDAR_MONTH,
                content=monthly_stats.build_monthly_view(),
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
