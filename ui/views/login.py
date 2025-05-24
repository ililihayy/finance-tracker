# Copyright (c) 2025 ililihayy. All rights reserved.

from typing import Any

import flet as ft  # type: ignore[import-not-found]
from flet_route import Basket, Params  # type: ignore[import-not-found]

from auth import Auth
from colors import LC
from database import Utils


def login_page(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    page.title = "Логін"
    page.window.width = 800
    page.window.height = 600
    page.theme = ft.Theme(text_theme=ft.TextTheme(
        body_medium=ft.TextStyle(color=LC.LIGHT_YELLOW)))

    title = ft.Text(
        "Вітаємо в Трекері Фінансів!",
        color=LC.LIGHT_YELLOW,
        size=24,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    login_txt = ft.Text(
        "Логін", color=LC.LIGHT_YELLOW, size=22, weight=ft.FontWeight.W_800, text_align=ft.TextAlign.CENTER
    )

    username = ft.TextField(
        label="Нікнейм",
        label_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
        focused_border_color=LC.LIGHT_YELLOW,
    )
    password = ft.TextField(
        label="Пароль",
        password=True,
        can_reveal_password=True,
        label_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
        focused_border_color=LC.LIGHT_YELLOW,
    )

    # Лічильник спроб
    attempts = 0

    def login_click(e: Any) -> None:
        nonlocal attempts
        username_val = username.value
        Auth.blocked_user = username_val
        user_status = Utils.get_user_status(username_val)
        if user_status == 1:
            page.open(ft.SnackBar(
                ft.Text("Акаунт заблокований. Спробуйте відновити пароль.")))
            return
        if attempts >= 3:
            page.open(ft.SnackBar(
                ft.Text("Акаунт заблокований. Спробуйте відновити пароль.")))
            Utils.block_user(username_val)
            page.update()
            return

        try:
            Auth.login_user(username_val, password.value)
            page.open(ft.SnackBar(ft.Text("Логін успішний!")))
            page.update()
            page.go("/expenses")
        except Exception:
            attempts += 1
            if attempts < 3:
                page.open(
                    ft.SnackBar(ft.Text(
                        f"Пароль або ім'я користувача неправильні. Залишилось спроб: {3 - attempts}"))
                )
            else:
                page.open(ft.SnackBar(
                    ft.Text("Обліковий запис заблоковано. Спробуйте скинути пароль.")))
            page.update()

    def forgot_password(e: Any) -> None:
        page.go("/forgot-password")

    def register(e: Any) -> None:
        page.go("/register")
        page.views.clear()

    login_button = ft.ElevatedButton(
        "Let's go!", on_click=login_click, bgcolor=LC.SUPER_DARK_GREEN, color=LC.LIGHT_YELLOW, width=140, height=35
    )

    forgot_button = ft.ElevatedButton(
        "Забув пароль",
        on_click=forgot_password,
        bgcolor=ft.Colors.TRANSPARENT,
        color=LC.LIGHT_YELLOW,
    )

    register_button = ft.ElevatedButton(
        "Реєстрація",
        on_click=register,
        bgcolor=ft.Colors.TRANSPARENT,
        color=LC.LIGHT_YELLOW,
    )

    attempt_text = ft.Text(
        "Спробувати можна тільки 3 рази. У разі невдачі ваш обліковий запис буде заблоковано.",
        color=LC.LIGHT_YELLOW,
        size=12,
        text_align=ft.TextAlign.CENTER,
    )

    container = ft.Container(
        content=ft.Column(
            [
                username,
                password,
                ft.Row([login_button], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([forgot_button, register_button],
                       alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                attempt_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        width=400,
        padding=ft.padding.all(20),
        bgcolor=LC.GREEN,
        border_radius=10,
    )

    main_container = ft.Container(
        content=ft.Column(
            [
                ft.Container(content=title, alignment=ft.alignment.center),
                ft.Container(content=login_txt, alignment=ft.alignment.center),
                ft.Container(height=20),
                ft.Container(content=container, alignment=ft.alignment.center),
            ],
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
    )

    return ft.View("/", controls=[main_container])
