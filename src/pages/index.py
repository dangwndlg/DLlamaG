from dash import html

def create_index_page(user: str) -> html.Div:
    return html.Div(f"Hello {user}")