# Copyright (c) 2025 ililihayy. All rights reserved.

import re
from typing import Any

import flet as ft  # type: ignore[import-not-found]
from flet_route import Basket, Params  # type: ignore[import-not-found]

from auth import Auth
from colors import RC
from . import confirmation as conf


def validate_username(username: str) -> tuple[bool, str]:
    if not username:
        return False, "Ім'я користувача не може бути порожнім"

    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]{2,19}$", username):
        return False, "Ім'я користувача повинно починатися з літери, містити 3-20 символів (літери, цифри, _)"

    return True, ""


def validate_email(email: str) -> tuple[bool, str]:
    if not email:
        return False, "Email не може бути порожнім"

    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, email):
        return False, "Невірний формат email"

    return True, ""


def validate_password(password: str) -> tuple[bool, str]:
    """Validate password:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    """
    if not password:
        return False, "Пароль не може бути порожнім"

    if len(password) < 8:
        return False, "Пароль повинен містити мінімум 8 символів"

    if not re.search(r"[A-Z]", password):
        return False, "Пароль повинен містити хоча б одну велику літеру"

    if not re.search(r"[a-z]", password):
        return False, "Пароль повинен містити хоча б одну малу літеру"

    if not re.search(r"[0-9]", password):
        return False, "Пароль повинен містити хоча б одну цифру"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, 'Пароль повинен містити хоча б один спеціальний символ (!@#$%^&*(),.?":{}|<>)'

    return True, ""


def register_page(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    page.title = "Реєстрація"
    page.window.width = 800
    page.window.height = 700
    page.theme = ft.Theme(text_theme=ft.TextTheme(body_medium=ft.TextStyle(color=RC.LIGHT_YELLOW)))

    username_error = ft.Text("", color="red", size=12)
    email_error = ft.Text("", color="red", size=12)
    password_error = ft.Text("", color="red", size=12)
    repeat_password_error = ft.Text("", color="red", size=12)

    reg_txt = ft.Text(
        "Реєстрація", color=RC.LIGHT_YELLOW, size=22, weight=ft.FontWeight.W_800, text_align=ft.TextAlign.CENTER
    )

    def validate_inputs() -> bool:
        is_valid = True

        # Validate username
        username_valid, username_msg = validate_username(username.value)
        username_error.value = username_msg
        username.border_color = "red" if not username_valid else RC.LIGHT_YELLOW
        is_valid = is_valid and username_valid

        # Validate email
        email_valid, email_msg = validate_email(email.value)
        email_error.value = email_msg
        email.border_color = "red" if not email_valid else RC.LIGHT_YELLOW
        is_valid = is_valid and email_valid

        # Validate password
        password_valid, password_msg = validate_password(password.value)
        password_error.value = password_msg
        password.border_color = "red" if not password_valid else RC.LIGHT_YELLOW
        is_valid = is_valid and password_valid

        # Validate password match
        if password.value != repeat_password.value:
            repeat_password_error.value = "Паролі не співпадають"
            repeat_password.border_color = "red"
            is_valid = False
        else:
            repeat_password_error.value = ""
            repeat_password.border_color = RC.LIGHT_YELLOW

        page.update()
        return is_valid

    username = ft.TextField(
        label="Ім'я користувача",
        label_style=ft.TextStyle(color=RC.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=RC.LIGHT_YELLOW),
        focused_border_color=RC.LIGHT_YELLOW,
        border_color=RC.LIGHT_YELLOW,
        on_change=lambda _: validate_inputs(),
    )

    email = ft.TextField(
        label="Email",
        label_style=ft.TextStyle(color=RC.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=RC.LIGHT_YELLOW),
        focused_border_color=RC.LIGHT_YELLOW,
        border_color=RC.LIGHT_YELLOW,
        on_change=lambda _: validate_inputs(),
    )

    password = ft.TextField(
        label="Пароль",
        password=True,
        can_reveal_password=True,
        label_style=ft.TextStyle(color=RC.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=RC.LIGHT_YELLOW),
        focused_border_color=RC.LIGHT_YELLOW,
        border_color=RC.LIGHT_YELLOW,
        on_change=lambda _: validate_inputs(),
    )

    repeat_password = ft.TextField(
        label="Повторіть пароль",
        password=True,
        can_reveal_password=True,
        label_style=ft.TextStyle(color=RC.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=RC.LIGHT_YELLOW),
        focused_border_color=RC.LIGHT_YELLOW,
        border_color=RC.LIGHT_YELLOW,
        on_change=lambda _: validate_inputs(),
    )

    def login_click(e: Any) -> None:
        page.go("/")

    def register(e: Any) -> None:
        if not validate_inputs():
            return

        username_val = username.value
        email_val = email.value

        conf.REGISTER_DATA = {
            "username": username_val,
            "email": email_val,
            "hash_password": Auth.hash_password(password.value),
        }
        page.go("/confirmation")

    reg_button = ft.ElevatedButton(
        "Реєстрація", on_click=register, bgcolor=RC.SUPER_DARK_GREEN, color=RC.LIGHT_YELLOW, width=140, height=35
    )

    login_button = ft.ElevatedButton(
        "Вхід",
        on_click=login_click,
        bgcolor=ft.colors.TRANSPARENT,
        color=RC.LIGHT_YELLOW,
    )

    container = ft.Container(
        content=ft.Column(
            [
                username,
                username_error,
                email,
                email_error,
                password,
                password_error,
                repeat_password,
                repeat_password_error,
                ft.Row([reg_button], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([login_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        width=400,
        padding=ft.padding.all(20),
        bgcolor=RC.GREEN,
        border_radius=10,
    )

    main_container = ft.Container(
        content=ft.Column(
            [
                ft.Container(content=reg_txt, alignment=ft.alignment.center),
                ft.Container(height=20),
                ft.Container(content=container, alignment=ft.alignment.center),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.BLACK,
        gradient=ft.LinearGradient(
            colors=[RC.SUPER_DARK_GREEN, RC.DARK_GREEN], begin=ft.alignment.top_left, end=ft.alignment.bottom_right
        ),
    )

    return ft.View("/register", controls=[main_container])
