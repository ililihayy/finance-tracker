import flet as ft  # type: ignore[import-not-found]
from flet_route import Routing  # type: ignore[import-not-found]

from start.at_start import create_db, create_env
from .middlewares.app_middleware import AppBasedMiddleware
from .routes import app_routes


def main(page: ft.Page) -> None:
    create_env()
    create_db()
    Routing(page=page, app_routes=app_routes, middleware=AppBasedMiddleware)
    page.go(page.route)


ft.app(target=main)
