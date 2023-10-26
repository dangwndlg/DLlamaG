from llama import Dialog
from pydantic import BaseModel

from typing import Awaitable, Callable, List, Literal

class DLlamaGResponse(BaseModel):
    last_message: str
    response: str
    
class DLlamaGDialog(BaseModel):
    role: str
    content: str

class DialogList(BaseModel):
    dialogs: List[DLlamaGDialog]

ChatCompleteFunction = Callable[[List[Dialog]], Awaitable[DLlamaGResponse]]

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
RequestType = Literal["chat", "health"]