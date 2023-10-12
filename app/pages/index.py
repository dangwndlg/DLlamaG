from dash import callback, dcc, html
from dash.dependencies import Input, Output, State

from utils import get_current_domino_user

from typing import Any, List, Optional, Tuple, Union

@callback(
    Output("current-user-header", "children"),
    Input("get-current-user-dummy", "children")
)
def current_user_header(_: Any) -> str:
    username: str = get_current_domino_user()
    return f"Welcome {username}"
                
@callback(
    [
        Output("chat-history-container", "children"),
        Output("chat-input", "value")
    ],
    [
        Input("chat-submit-button", "n_clicks"),
        Input("chat-input", "n_submit")
    ],
    State("chat-input", "value"),
    State("chat-history-container", "children")
)
def update_output_and_clear_input(
    n_clicks: int,
    n_submit: Optional[int], 
    input_value: str, 
    current_output: Optional[List[html.Div]]
) -> Tuple[Union[Optional[List[html.Div]], str]]:
    if n_clicks > 0 or bool(n_submit):
        if input_value:
            new_output = html.Div(input_value, style={"margin-bottom": "10px"})
            return ([new_output] + current_output if current_output else [new_output], "")
    return current_output, input_value

def create_index_page() -> html.Div:
    return html.Div(children=[
        html.H1(id="current-user-header"),

        dcc.Input(id="chat-input", type="text", placeholder="Enter text..."),
        html.Button("Submit", id="chat-submit-button", n_clicks=0),
        dcc.Loading(
            id="loading-chat-history-container",
            type="circle",
            children=[html.Div(id="chat-history-container")],
        ),

        html.Div(id="get-current-user-dummy", style={"display": "none"})
    ])