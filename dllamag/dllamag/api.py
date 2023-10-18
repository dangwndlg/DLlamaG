from fire import Fire
from fire.core import FireError, FireExit
from requests.exceptions import ConnectionError

from dllamag.config import API_HOST, API_VERSION, MAX_SEQ_LEN
from dllamag.custom_types import DLlamaGDialog
from dllamag.dlg_requests import DLGRequestManager
from dllamag.exceptions import APIError, ConfigError

from requests import Response
from typing import Any, Dict, List, Optional

class DLlamaG:
    def __init__(self, system_prompt: Optional[str] = None):        
        self._health_endpoint: str = f"{API_HOST}/{API_VERSION}/health"
        self._chat_endpoint: str = f"{API_HOST}/{API_VERSION}/chat"
        
        self.session: DLGRequestManager = DLGRequestManager()

        if not self._health_check():
            raise ConfigError("Health check returned unexpected response...")
        
        self.system_prompt = system_prompt
        self.chat_history: List[DLlamaGDialog] = []

        self._num_chats: int = self._calculate_num_chats()
        self._current_message_id: int = 0
    
    def _append_dialog(self, role: str, content: str) -> None:
        # Will replace end dialog if the role is the same
        if self._current_message_id > 0:
            if self.chat_history[-1].role == role:
                self.chat_history[-1].content = content
                return
            
        self.chat_history.append(DLlamaGDialog(
            message_id=self._current_message_id,
            role=role,
            content=content,
            system_prompt=self.system_prompt
        ))
        self._current_message_id += 1

    def _calculate_num_chats(self) -> int:
        # Prompts are sent (s/)u/a/u/a/.../u
        if (self.system_prompt and MAX_SEQ_LEN%2) \
            or not(self.system_prompt or MAX_SEQ_LEN%2):
            return MAX_SEQ_LEN-1
        return MAX_SEQ_LEN

    def _chat(self) -> None:
        print("""
Welcome to DLlamaG! To exit chat, enter "exit()" in the input box.
You can clear your history by exiting chat and running the 
    "clear_chat_history" method, or you can use a new system prompt 
    by using the "set_system_prompt" method.
        """)

        while True:
            msg: str = input("> ")
            
            if msg == "exit()":
                break

            response: Optional[str] = self.message(msg=msg)
            if not response:
                break
            print(f"Assistant: {response}")

    def _compile_dialog_payload(self) -> List[Dict[str, str]]:
        payload: List[Dict[str, str]] = []
        
        if self.system_prompt:
            payload.append({
                "role": "system",
                "content": self.system_prompt
            })

        payload += [{
            "role": chat.role,
            "content": chat.content
        } for chat in self.chat_history[-self._num_chats:]]

        return payload
    
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
    
    def _send_dialogs(self) -> str:
        payload: Dict[str, Any] = {
            "dialogs": self._compile_dialog_payload()
        }

        try:
            response: Response = self.session.post(
                url=self._chat_endpoint,
                json=payload
            )
            if response.status_code != 200:
                raise ValueError
        
            return response.json()["response"]
        except ValueError:
            raise APIError("DLlamaG returned a non 200 status code")
        except ConnectionError:
            raise APIError(f"Could not reach DLlamaG API at {API_HOST}/{API_VERSION}")
        except Exception as e:
            raise APIError(f"Could not retrieve response due to error: {e}")

    def chat(self) -> None:
        # Fire(self._chat())
        self._chat()

    def clear_chat_history(self, clear_system_prompt: bool = False) -> None:
        self.chat_history = []
        self._current_message_id = 0
        if clear_system_prompt:
            self.system_prompt = None
            self._num_chats = self._calculate_num_chats()

    def message(self, msg: str) -> Optional[str]:
        self._append_dialog(role="user", content=msg)

        try:
            response: str = self._send_dialogs()
            self._append_dialog(role="assistant", content=response)
            return response
        except Exception as e:
            print(f"There was a problem getting your response...")
            print(e)

        return None

    def set_system_prompt(self, prompt: Optional[str] = None) -> None:
        self.system_prompt = prompt
        self._num_chats = self._calculate_num_chats()
