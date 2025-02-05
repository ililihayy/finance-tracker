import flet as ft  # type: ignore[import-not-found]
from flet_route import Routing  # type: ignore[import-not-found]

from .middlewares.app_middleware import AppBasedMiddleware
from .routes import app_routes


def main(page: ft.Page) -> None:
    Routing(page=page, app_routes=app_routes, middleware=AppBasedMiddleware)
    page.go(page.route)


ft.app(target=main)
