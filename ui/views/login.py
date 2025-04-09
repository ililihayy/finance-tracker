# Copyright (c) 2025 ililihayy. All rights reserved.

from typing import Any

import flet as ft  # type: ignore[import-not-found]
from flet_route import Basket, Params  # type: ignore[import-not-found]

from colors import LC


def login_page(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    page.title = "Login"
    page.window.width = 800
    page.window.height = 600
    page.theme = ft.Theme(text_theme=ft.TextTheme(body_medium=ft.TextStyle(color=LC.LIGHT_YELLOW)))

    title = ft.Text(
        "Welcome to Finance Tracker!",
        color=LC.LIGHT_YELLOW,
        size=24,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    login_txt = ft.Text(
        "Login", color=LC.LIGHT_YELLOW, size=22, weight=ft.FontWeight.W_800, text_align=ft.TextAlign.CENTER
    )

    username = ft.TextField(
        label="Username",
        label_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
        focused_border_color=LC.LIGHT_YELLOW,
    )
    password = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        label_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
        focused_border_color=LC.LIGHT_YELLOW,
    )

    def login_click(e: Any) -> None:
        page.go("/register")

    def forgot_password(e: Any) -> None:
        page.go("/forgot-password")

    def register(e: Any) -> None:
        page.go("/register")
        page.views.clear()

    login_button = ft.ElevatedButton(
        "Let's go!", on_click=login_click, bgcolor=LC.SUPER_DARK_GREEN, color=LC.LIGHT_YELLOW, width=140, height=35
    )

    forgot_button = ft.ElevatedButton(
        "Forgot password",
        on_click=forgot_password,
        bgcolor=ft.colors.TRANSPARENT,
        color=LC.LIGHT_YELLOW,
    )

    register_button = ft.ElevatedButton(
        "Registration",
        on_click=register,
        bgcolor=ft.colors.TRANSPARENT,
        color=LC.LIGHT_YELLOW,
    )

    container = ft.Container(
        content=ft.Column(
            [
                username,
                password,
                ft.Row([login_button], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([forgot_button, register_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
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
        bgcolor=ft.colors.BLACK,
        gradient=ft.LinearGradient(
            colors=[LC.SUPER_DARK_GREEN, LC.DARK_GREEN], begin=ft.alignment.top_left, end=ft.alignment.bottom_right
        ),
    )

    return ft.View("/", controls=[main_container])
