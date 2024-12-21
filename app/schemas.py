from pydantic import BaseModel
from typing import List

class ChatMessage(BaseModel):
    message: str

class DocumentInput(BaseModel):
    texts: List[str]