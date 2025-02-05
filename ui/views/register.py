# Copyright (c) 2025 ililihayy. All rights reserved.

from typing import Any

import flet as ft  # type: ignore[import-not-found]
from flet_route import Basket, Params  # type: ignore[import-not-found]

from colors import RC


def register_page(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    page.title = "Login"
    page.window.width = 800
    page.window.height = 600
    page.theme = ft.Theme(text_theme=ft.TextTheme(body_medium=ft.TextStyle(color=RC.LIGHT_YELLOW)))

    reg_txt = ft.Text(
        "Registration", color=RC.LIGHT_YELLOW, size=22, weight=ft.FontWeight.W_800, text_align=ft.TextAlign.CENTER
    )

    username = ft.TextField(
        label="Username",
        label_style=ft.TextStyle(color=RC.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=RC.LIGHT_YELLOW),
        focused_border_color=RC.LIGHT_YELLOW,
    )
    email = ft.TextField(
        label="Email",
        label_style=ft.TextStyle(color=RC.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=RC.LIGHT_YELLOW),
        focused_border_color=RC.LIGHT_YELLOW,
    )
    password = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        label_style=ft.TextStyle(color=RC.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=RC.LIGHT_YELLOW),
        focused_border_color=RC.LIGHT_YELLOW,
    )
    repeat_password = ft.TextField(
        label="Repeat password",
        password=True,
        can_reveal_password=True,
        label_style=ft.TextStyle(color=RC.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=RC.LIGHT_YELLOW),
        focused_border_color=RC.LIGHT_YELLOW,
    )

    def login_click(e: Any) -> None:
        page.go("/")

    def register(e: Any) -> None:
        pass

    reg_button = ft.ElevatedButton(
        "Registration", on_click=register, bgcolor=RC.SUPER_DARK_GREEN, color=RC.LIGHT_YELLOW, width=140, height=35
    )

    login_button = ft.ElevatedButton(
        "Login",
        on_click=login_click,
        bgcolor=ft.colors.TRANSPARENT,
        color=RC.LIGHT_YELLOW,
    )

    container = ft.Container(
        content=ft.Column(
            [
                username,
                email,
                password,
                repeat_password,
                ft.Row([reg_button], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([login_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
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
