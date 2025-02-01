# Copyright (c) 2025 ililihayy. All rights reserved.

from typing import Any

import flet as ft  # type: ignore[import-not-found]

from colors import Col


def main(page: ft.Page) -> None:
    page.title = "Login"

    page.window.width = 800
    page.window.height = 600
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme = ft.Theme(text_theme=ft.TextTheme(body_medium=ft.TextStyle(color=Col.LIGHT_YELLOW)))
    page.bgcolor = ft.colors.TRANSPARENT
    page.decoration = ft.BoxDecoration(
        gradient=ft.LinearGradient(
            colors=[Col.SUPER_DARK_GREEN, Col.DARK_GREEN], begin=ft.alignment.top_left, end=ft.alignment.bottom_right
        )
    )

    title = ft.Text(
        "Welcome to Finance Tracker!",
        color=Col.LIGHT_YELLOW,
        size=24,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    login_txt = ft.Text(
        "Login", color=Col.LIGHT_YELLOW, size=22, weight=ft.FontWeight.W_800, text_align=ft.TextAlign.CENTER
    )

    page.add(title)
    page.add(ft.Container(height=20))
    page.add(login_txt)

    username = ft.TextField(
        label="Username",
        label_style=ft.TextStyle(color=Col.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=Col.LIGHT_YELLOW),
        focused_border_color=Col.LIGHT_YELLOW,
    )
    password = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        label_style=ft.TextStyle(color=Col.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=Col.LIGHT_YELLOW),
        focused_border_color=Col.LIGHT_YELLOW,
    )

    def login_click(e: Any) -> None:
        pass

    def forgot_password(e: Any) -> None:
        pass

    def register(e: Any) -> None:
        pass

    login_button = ft.ElevatedButton(
        "Let's go!", on_click=login_click, bgcolor=Col.SUPER_DARK_GREEN, color=Col.LIGHT_YELLOW, width=140, height=35
    )

    forgot_button = ft.ElevatedButton(
        "Forgot password",
        on_click=forgot_password,
        bgcolor=ft.colors.TRANSPARENT,
        color=Col.LIGHT_YELLOW,
    )

    register_button = ft.ElevatedButton(
        "Registration",
        on_click=register,
        bgcolor=ft.colors.TRANSPARENT,
        color=Col.LIGHT_YELLOW,
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
        bgcolor=Col.GREEN,
        border_radius=10,
    )
    page.add(ft.Container(height=5))
    page.add(container)


ft.app(target=main)
