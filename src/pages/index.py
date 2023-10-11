from dash import callback, html
from dash.dependencies import Input, Output

from utils import get_current_domino_user

from typing import Any

@callback(
    Output("current-user-header", "children"),
    Input("get-current-user-dummy", "children")
)
def current_user_header(_: Any) -> str:
    username: str = get_current_domino_user()
    return f"Welcome {username}"

def create_index_page() -> html.Div:
    return html.Div(children=[
        html.H1(id="current-user-header"),

        html.Div(id="get-current-user-dummy", style={"display": "none"})
    ])