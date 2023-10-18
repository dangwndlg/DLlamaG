from pydantic import BaseModel
from typing import Optional

class DLlamaGDialog(BaseModel):
    message_id: int
    role: str
    content: str
    system_prompt: Optional[str]