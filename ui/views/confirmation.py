# Copyright (c) 2025 ililihayy. All rights reserved.

from typing import Any

import flet as ft  # type: ignore[import-not-found]
from flet_route import Basket, Params  # type: ignore[import-not-found]

from auth import Auth
from auth.exceptions import ConfirmCodeError
from colors import RC
from database.exceptions import UserAlreadyExistError

REGISTER_DATA: dict[str, str] = {}


def confirmation_page(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    page.title = "Підтвердження електронної пошти"
    page.window.width = 800
    page.window.height = 600
    page.theme = ft.Theme(text_theme=ft.TextTheme(body_medium=ft.TextStyle(color=RC.LIGHT_YELLOW)))

    email = REGISTER_DATA["email"]
    print(email)
    Auth.send_confirmation_email(email)

    confirmation_txt = ft.Text(
        "Підтвердження електронної пошти",
        color=RC.LIGHT_YELLOW,
        size=22,
        weight=ft.FontWeight.W_800,
        text_align=ft.TextAlign.CENTER,
    )

    info_text = ft.Text(
        "Код підтвердження надіслано на вашу пошту.",
        color=RC.LIGHT_YELLOW,
        size=14,
        text_align=ft.TextAlign.CENTER,
    )

    code_field = ft.TextField(
        label="Код підтвердження",
        label_style=ft.TextStyle(color=RC.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=RC.LIGHT_YELLOW),
        focused_border_color=RC.LIGHT_YELLOW,
    )

    def show_notification(message: str, color: str = RC.LIGHT_YELLOW) -> None:
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=color),
            bgcolor=RC.GREEN,
            duration=3000,
        )
        page.snack_bar.open = True
        page.update()

    def submit_click(e: Any) -> None:
        code = code_field.value
        if not code:
            show_notification("Будь ласка, введіть код підтвердження")
            return

        try:
            Auth.register_user(
                REGISTER_DATA["username"],
                REGISTER_DATA["email"],
                REGISTER_DATA["hash_password"],
                code,
            )
            show_notification("Реєстрація успішна! Тепер ви можете увійти в систему.")
            page.update()
            page.go("/")
            page.views.clear()
        except UserAlreadyExistError:
            show_notification("Користувач з таким ім'ям або email вже існує")
        except ConfirmCodeError as err:
            if "Invalid confirmation code" in str(err):
                show_notification("Невірний код підтвердження")
            else:
                show_notification(str(err))

    def resend_code(e: Any) -> None:
        try:
            Auth.send_confirmation_email(REGISTER_DATA["email"])
            show_notification("Новий код підтвердження надіслано на вашу електронну пошту")
        except Exception as err:
            show_notification(f"Помилка при відправці коду: {err!s}")

    def register(e: Any) -> None:
        page.go("/register")

    submit_button = ft.ElevatedButton(
        "Підтвердити код",
        on_click=submit_click,
        bgcolor=RC.SUPER_DARK_GREEN,
        color=RC.LIGHT_YELLOW,
        width=140,
        height=35,
    )

    resend_code_button = ft.TextButton(
        "Надіслати код знову",
        on_click=resend_code,
        style=ft.ButtonStyle(color=ft.colors.WHITE),
    )

    register_button = ft.TextButton(
        "Реєстрація",
        on_click=register,
        style=ft.ButtonStyle(color=ft.colors.WHITE),
    )

    container = ft.Container(
        content=ft.Column(
            [
                code_field,
                ft.Row([submit_button], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(
                    [register_button, resend_code_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=35,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        width=400,
        padding=ft.padding.all(20),
        bgcolor=RC.GREEN,
        border_radius=10,
    )

    main_container = ft.Container(
        content=ft.Column(
            [
                ft.Container(content=confirmation_txt, alignment=ft.alignment.center),
                ft.Container(height=10),
                ft.Container(content=info_text, alignment=ft.alignment.center),
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

    return ft.View("/confirm", controls=[main_container])
