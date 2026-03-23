# backend/app/ai_orchestration/agents/responder_agent.py
from app.infrastructure.llm.provider_router import ProviderRouter

class ResponderAgent:
    async def generate(self, message: str) -> str:
        provider = ProviderRouter().get_provider()
        return await provider.generate(message)