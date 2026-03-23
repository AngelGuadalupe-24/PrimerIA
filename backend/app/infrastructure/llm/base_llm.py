# backend/app/infrastructure/llm/base_llm.py
from abc import ABC, abstractmethod

class BaseLLM(ABC):
    @abstractmethod
    async def generate(self, prompt: str, context: dict | None = None) -> str:
        """
        Genera respuesta a partir de un prompt.
        Todos los LLM deben implementar este método.
        """
        pass