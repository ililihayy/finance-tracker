from flet_route import path  # type: ignore[import-not-found]

from .middlewares.url_middleware import UrlBasedMiddleware
from .views.confirmation import confirmation_page
from .views.forgot_password import forgot_password_page
from .views.login import login_page
from .views.register import register_page

app_routes = [
    path(url="/", clear=True, view=login_page),
    path(url="/register", clear=False, view=register_page, middleware=UrlBasedMiddleware),
    path(url="/forgot-password", clear=False, view=forgot_password_page, middleware=UrlBasedMiddleware),
    path(url="/confirmation", clear=False, view=confirmation_page, middleware=UrlBasedMiddleware),
]
