# backend/app/interface/http/test_llm.py

from fastapi import APIRouter
from app.ai_orchestration.agents.responder_agent import ResponderAgent
from pydantic import BaseModel

router = APIRouter()

class MessageRequest(BaseModel):
    message: str

@router.post("/test_llm/")
async def test_llm(request: MessageRequest):
    agent = ResponderAgent()
    response = await agent.generate(request.message)
    return {"response": response}