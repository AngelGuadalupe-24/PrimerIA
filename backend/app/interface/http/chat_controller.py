# backend/app/interface/http/chat_controller.py

from fastapi import APIRouter

# Imports absolutos
from app.application.use_cases.process_chat import ProcessChatUseCase
from app.application.dto.chat_dto import ChatRequestDTO, ChatResponseDTO

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/")
async def chat(request: ChatRequestDTO):
    use_case = ProcessChatUseCase()
    response = await use_case.execute(request)
    return response