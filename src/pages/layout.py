from dash import html

from pages.index import create_index_page

def create_layout() -> html.Div:
    return create_index_page()
