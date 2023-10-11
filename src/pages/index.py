from dash import html
from flask import request

def create_index_page() -> html.Div:
    user: str = request.headers.get("domino-username", "UNKNOWN")

    return html.Div(f"Hello {user}")