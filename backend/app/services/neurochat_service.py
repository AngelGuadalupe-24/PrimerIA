# backend/app/services/neurochat_service.py

from app.ai_orchestration.brain import Brain

class NeuroChatService:
    def __init__(self, llm_provider=None):
        """
        llm_provider: instancia de cualquier proveedor LLM (Ollama, OpenAI, Gemini, Mock)
        """
        self.brain = Brain(llm_provider=llm_provider)

    async def process_message(self, message: str, user_id: str):
        # Usar el método think() que ahora Brain expone
        response_text = await self.brain.think(message)
        return {"response": response_text}