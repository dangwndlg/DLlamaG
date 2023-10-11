from pydantic import BaseModel

class DLlamaGResponse(BaseModel):
    last_message: str
    response: str
    error: str