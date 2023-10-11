from dash import Dash
import os

from typing import Optional

from exceptions import AppConfigError
from pages.layout import create_layout

def construct_domino_run_url() -> Optional[str]:
    try:
        user: str = os.environ["DOMINO_PROJECT_OWNER"]
        project: str = os.environ["DOMINO_PROJECT_NAME"]
        run_id: str = os.environ["DOMINO_RUN_ID"]

        return f"/{user}/{project}/r/notebookSession/{run_id}/"
    except KeyError as e:
        raise AppConfigError(f"Error when retrieving url environment variables: {e}")
    except Exception as e:
        raise AppConfigError(f"Error when constructing run url: {e}")
    
class LlamaApp(Dash):
    def __init__(self, *args, **kwargs) -> None:
        super(LlamaApp, self).__init__(*args, **kwargs)

        self.layout = create_layout()