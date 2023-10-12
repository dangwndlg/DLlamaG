from llama import Dialog
from pydantic import BaseModel

from typing import Awaitable, Callable, List

class DLlamaGResponse(BaseModel):
    last_message: str
    response: str
    
class DLlamaGDialog(BaseModel):
    role: str
    content: str

class DialogList(BaseModel):
    dialogs: List[DLlamaGDialog]

ChatCompleteFunction = Callable[[List[Dialog]], Awaitable[DLlamaGResponse]]