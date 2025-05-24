import flet as ft  # type: ignore[import-not-found]
from flet_route import Routing  # type: ignore[import-not-found]

from security.key import ensure_encryption_key
from start.at_start import create_db, create_env
from ui.middlewares.app_middleware import AppBasedMiddleware
from ui.routes import app_routes


def main(page: ft.Page) -> None:
    create_env()
    create_db()
    # ensure_encryption_key()
    Routing(page=page, app_routes=app_routes, middleware=AppBasedMiddleware)
    page.go(page.route)


ft.app(target=main)
