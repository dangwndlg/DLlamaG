try:
    import fire
except ImportError:
    raise ImportError("Must have fire installed - run 'pip install fire --upgrade --user' to install")

from app import construct_domino_run_url, LlamaApp
from config import IS_DOMINO_ENV

from typing import Dict

def main() -> None:
    app_kwargs: Dict[str, str] = {
        "name": __name__
    }

    if IS_DOMINO_ENV:
        app_kwargs.update({
            "routes_pathname_prefix": "/",
            "requests_pathname_prefix": construct_domino_run_url()
        })

    app: LlamaApp = LlamaApp(**app_kwargs)
    app.run_server(host="0.0.0.0", port=8888, debug=True)

if __name__ == "__main__":
    fire.Fire(main())