# backend/app/infrastructure/llm/mock_provider.py
from app.infrastructure.llm.base_llm import BaseLLM

class MockProvider(BaseLLM):
    """
    Proveedor mock para pruebas locales.
    Devuelve respuestas simuladas.
    """
    def __init__(self):
        self.counter = 0

    async def generate(self, prompt: str) -> str:
        self.counter += 1
        return f"[Mock {self.counter}] Respuesta a: {prompt}"