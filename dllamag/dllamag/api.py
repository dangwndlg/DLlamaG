from requests.exceptions import ConnectionError

from dllamag.config import API_HOST, API_VERSION
from dllamag.dlg_requests import DLGRequestManager
from dllamag.exceptions import APIError, ConfigError

from requests import Response

class DLlamaG:
    def __init__(self):        
        self._health_endpoint: str = f"{API_HOST}/{API_VERSION}/health"
        self._chat_endpoint: str = f"{API_HOST}/{API_VERSION}/chat"
        
        self.session: DLGRequestManager = DLGRequestManager()

        if self._health_check() != True:
            raise ConfigError("Health check returned unexpected response...")
        


    def _health_check(self) -> bool:
        try:
            response: Response = self.session.get(self._health_endpoint)
            if response.status_code != 200 or response.json()["success"] != True:
                raise APIError("Could not successfully verify DLlamaG API health check")
        except ConnectionError:
            raise APIError(f"Could not reach DLlamaG API at {API_HOST}/{API_VERSION}")
        except Exception as e:
            raise ConfigError(f"Could not initialize DLlamaG due to error: {e}")
        
        return True