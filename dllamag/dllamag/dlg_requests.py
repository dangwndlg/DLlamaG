from requests import Response, Session

class DLGRequestManager:
    def __init__(self, verify: bool = True) -> None:
        self.request_manager: Session = Session()

        if not verify:
            self.request_manager.verify = False

    def get(self, url: str, **kwargs) -> Response:
        return self.request_manager.get(url=url, **kwargs)

    def post(self, url: str, **kwargs) -> Response:
        return self.request_manager.post(url=url, **kwargs)
