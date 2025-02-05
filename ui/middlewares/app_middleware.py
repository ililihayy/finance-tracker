import flet as ft  # type: ignore[import-not-found]
from flet_route import Basket, Params  # type: ignore[import-not-found]


def AppBasedMiddleware(page: ft.Page, params: Params, basket: Basket) -> None:
    print("App Based Middleware Called")
    # page.route = "/another_view" # If you want to change the route for some reason, use page.route
