from dash import html
from flask import request

from pages.index import create_index_page

def create_layout() -> html.Div:
    user: str = request.headers.get("domino-username", "UNKNOWN")

    return create_index_page(user=user)
