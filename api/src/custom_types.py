from pydantic import BaseModel

from typing import Dict, List

class DLlamaGResponse(BaseModel):
    last_message: str
    response: str
    
class DLlamaGDialog(BaseModel):
    role: str
    content: str

class DialogList(BaseModel):
    dialogs: List[DLlamaGDialog]