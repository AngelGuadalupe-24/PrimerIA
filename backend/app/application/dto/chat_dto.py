# application/dto/chat_dto.py

from pydantic import BaseModel

class ChatRequestDTO(BaseModel):
    user_id: str
    message: str

class ChatResponseDTO(BaseModel):
    response: str