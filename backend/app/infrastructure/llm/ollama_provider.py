# ollama_provider.py

import httpx
import os
import logging
from app.infrastructure.llm.base_llm import BaseLLM

logger = logging.getLogger("ollama_provider")


class OllamaProvider(BaseLLM):

    def __init__(self):
        self.url = os.getenv(
            "OLLAMA_URL",
            "http://ollama:11434/api/generate"  # 🔥 FIX CLAVE
        )
        self.model = os.getenv("OLLAMA_MODEL", "llama3")

        self.client = httpx.AsyncClient(timeout=20)

    async def generate(self, prompt: str, context: dict | None = None) -> str:

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = await self.client.post(self.url, json=payload)

            response.raise_for_status()
            data = response.json()

            if "response" in data:
                return data["response"]

            logger.warning("Respuesta sin campo 'response'")
            return "No se pudo generar respuesta."

        except httpx.TimeoutException:
            logger.error("Timeout con Ollama")
            return "El modelo tardó demasiado en responder."

        except httpx.HTTPError as e:
            logger.error(f"Error HTTP: {e}")
            return "Error al contactar el modelo."

        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            return "Error interno al generar la respuesta."

    async def close(self):
        await self.client.aclose()