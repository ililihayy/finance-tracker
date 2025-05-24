# Copyright (c) 2025 ililihayy. All rights reserved.

from typing import Any

import flet as ft  # type: ignore[import-not-found]
from flet_route import Basket, Params  # type: ignore[import-not-found]

from auth import Auth
from colors import LC
from database.utils import Utils


def forgot_password_page(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    page.title = "Відновлення паролю"
    page.window.width = 800
    page.window.height = 600
    page.theme = ft.Theme(text_theme=ft.TextTheme(
        body_medium=ft.TextStyle(color=LC.LIGHT_YELLOW)))

    def show_notification(message: str, is_error: bool = False) -> None:
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=LC.LIGHT_YELLOW),
            bgcolor=LC.GREEN,
            duration=3000,
        )
        page.snack_bar.open = True
        page.update()

    def validate_password(password: str) -> tuple[bool, str]:
        if len(password) < 8:
            return False, "Пароль повинен містити мінімум 8 символів"
        if not any(c.isupper() for c in password):
            return False, "Пароль повинен містити хоча б одну велику літеру"
        if not any(c.islower() for c in password):
            return False, "Пароль повинен містити хоча б одну малу літеру"
        if not any(c.isdigit() for c in password):
            return False, "Пароль повинен містити хоча б одну цифру"
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            return False, "Пароль повинен містити хоча б один спеціальний символ"
        return True, ""

    def send_code(e: Any) -> None:
        email = Utils.get_user_email(Auth.blocked_user)
        try:
            Auth.send_confirmation_email(email)
            show_notification("Код підтвердження надіслано на вашу пошту")
            code_field.disabled = False
            new_password.disabled = False
            confirm_password.disabled = False
            reset_button.disabled = False
            page.update()
        except ValueError as err:
            show_notification(str(err), True)
            code_field.disabled = True
            new_password.disabled = True
            confirm_password.disabled = True
            reset_button.disabled = True
            page.update()
        except Exception as err:
            show_notification(f"Помилка при відправці коду: {err!s}", True)
            code_field.disabled = True
            new_password.disabled = True
            confirm_password.disabled = True
            reset_button.disabled = True
            page.update()

    def reset_password(e: Any) -> None:
        email = Utils.get_user_email(Auth.blocked_user)
        code = code_field.value
        new_pass = new_password.value
        confirm_pass = confirm_password.value

        if not all([email, code, new_pass, confirm_pass]):
            show_notification("Будь ласка, заповніть всі поля", True)
            return

        if new_pass != confirm_pass:
            show_notification("Паролі не співпадають!", True)
            return

        is_valid, error_msg = validate_password(new_pass)
        if not is_valid:
            show_notification(error_msg, True)
            return

        Utils.unblock_user(Auth.blocked_user)
        show_notification("Пароль успішно змінено!")
        code_field.value = ""
        new_password.value = ""
        confirm_password.value = ""
        code_field.disabled = True
        new_password.disabled = True
        confirm_password.disabled = True
        reset_button.disabled = True
        page.update()
        page.go("/")

    def back_to_login(e: Any) -> None:
        page.go("/")

    title = ft.Text(
        "Відновлення паролю",
        color=LC.LIGHT_YELLOW,
        size=24,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    code_field = ft.TextField(
        label="Код підтвердження",
        label_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
        focused_border_color=LC.LIGHT_YELLOW,
        width=250,
        disabled=True,
    )

    code_row = ft.Row(
        controls=[
            code_field,
            ft.ElevatedButton(
                "Надіслати код",
                on_click=send_code,
                bgcolor=LC.SUPER_DARK_GREEN,
                color=LC.LIGHT_YELLOW,
                height=40,
                width=130,
            ),
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        width=400,
    )

    new_password = ft.TextField(
        label="Новий пароль",
        password=True,
        can_reveal_password=True,
        label_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
        focused_border_color=LC.LIGHT_YELLOW,
        width=400,
        disabled=True,
    )

    confirm_password = ft.TextField(
        label="Підтвердження паролю",
        password=True,
        can_reveal_password=True,
        label_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
        focused_border_color=LC.LIGHT_YELLOW,
        width=400,
        disabled=True,
    )

    reset_button = ft.ElevatedButton(
        "Змінити пароль",
        on_click=reset_password,
        bgcolor=LC.SUPER_DARK_GREEN,
        color=LC.LIGHT_YELLOW,
        width=200,
        height=40,
        disabled=True,
    )

    back_button = ft.TextButton(
        "Повернутися до входу", on_click=back_to_login, style=ft.ButtonStyle(color=LC.LIGHT_YELLOW)
    )

    form_column = ft.Column(
        [
            code_row,
            new_password,
            confirm_password,
            ft.Container(height=10),
            ft.Row([reset_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([back_button], alignment=ft.MainAxisAlignment.CENTER),
        ],
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        width=400,
    )

    main_container = ft.Container(
        content=ft.Column(
            [ft.Container(content=title, padding=ft.padding.only(
                bottom=30)), form_column],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.BLACK,
        gradient=ft.LinearGradient(
            colors=[LC.SUPER_DARK_GREEN,
                    LC.DARK_GREEN], begin=ft.alignment.top_left, end=ft.alignment.bottom_right
        ),
        padding=ft.padding.all(20),
    )

    return ft.View("/forgot-password", controls=[main_container])
