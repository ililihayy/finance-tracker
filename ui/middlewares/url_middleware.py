import flet as ft  # type: ignore[import-not-found]
from flet_route import Basket, Params  # type: ignore[import-not-found]


def UrlBasedMiddleware(page: ft.Page, params: Params, basket: Basket) -> None:
    print("Url Based Middleware Called")
    # page.route = "/another_view" # If you want to change the route for some reason, use page.route
