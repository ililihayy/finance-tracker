# Copyright (c) 2025 ililihayy. All rights reserved.

from typing import Any

import flet as ft  # type: ignore[import-not-found]
from flet_route import Basket, Params  # type: ignore[import-not-found]

from colors import LC


def forgot_password_page(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    page.title = "Password Recovery"
    page.window.width = 800
    page.window.height = 600
    page.theme = ft.Theme(text_theme=ft.TextTheme(body_medium=ft.TextStyle(color=LC.LIGHT_YELLOW)))

    def send_code(e: Any) -> None:
        page.snack_bar = ft.SnackBar(ft.Text("The confirmation code has been sent to your mail"))
        page.snack_bar.open = True
        page.update()

    def reset_password(e: Any) -> None:
        if new_password.value != confirm_password.value:
            page.snack_bar = ft.SnackBar(ft.Text("Passwords do not match!"))
            page.snack_bar.open = True
            page.update()
            return

        page.snack_bar = ft.SnackBar(ft.Text("The password has been successfully changed!"))
        page.snack_bar.open = True
        page.update()
        page.go("/")

    def back_to_login(e: Any) -> None:
        page.go("/")

    title = ft.Text(
        "Recover your password",
        color=LC.LIGHT_YELLOW,
        size=24,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    email_field = ft.TextField(
        label="E-mail",
        label_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
        focused_border_color=LC.LIGHT_YELLOW,
        keyboard_type=ft.KeyboardType.EMAIL,
        width=400,
    )

    code_row = ft.Row(
        controls=[
            ft.TextField(
                label="Confirmation code",
                label_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
                text_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
                focused_border_color=LC.LIGHT_YELLOW,
                width=250,
                expand=True,
            ),
            ft.ElevatedButton(
                "Send the code",
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
        label="New password",
        password=True,
        can_reveal_password=True,
        label_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
        focused_border_color=LC.LIGHT_YELLOW,
        width=400,
    )

    confirm_password = ft.TextField(
        label="Confirm the password",
        password=True,
        can_reveal_password=True,
        label_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
        text_style=ft.TextStyle(color=LC.LIGHT_YELLOW),
        focused_border_color=LC.LIGHT_YELLOW,
        width=400,
    )

    reset_button = ft.ElevatedButton(
        "Change the password",
        on_click=reset_password,
        bgcolor=LC.SUPER_DARK_GREEN,
        color=LC.LIGHT_YELLOW,
        width=200,
        height=40,
    )

    back_button = ft.TextButton(
        "Go back to the entrance", on_click=back_to_login, style=ft.ButtonStyle(color=LC.LIGHT_YELLOW)
    )

    form_column = ft.Column(
        [
            email_field,
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
            [ft.Container(content=title, padding=ft.padding.only(bottom=30)), form_column],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.BLACK,
        gradient=ft.LinearGradient(
            colors=[LC.SUPER_DARK_GREEN, LC.DARK_GREEN], begin=ft.alignment.top_left, end=ft.alignment.bottom_right
        ),
        padding=ft.padding.all(20),
    )

    return ft.View("/forgot-password", controls=[main_container])
