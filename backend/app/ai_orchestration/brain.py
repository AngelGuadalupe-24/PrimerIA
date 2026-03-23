# backend/app/ai_orchestration/brain.py

import asyncio
import logging
import time
from typing import Optional

from app.infrastructure.llm.provider_router import ProviderRouter

logger = logging.getLogger("brain")


class Brain:
    def __init__(self, llm_provider=None, provider_type: str = "ollama"):
        try:
            self.provider = llm_provider or ProviderRouter(provider_type).get_provider()
            self.provider_name = type(self.provider).__name__
            logger.info(f"[Brain] Provider activo: {self.provider_name}")
        except Exception as e:
            logger.critical(f"[Brain] Error inicializando provider: {e}")
            self.provider = None
            self.provider_name = "None"

    async def think(self, prompt: str) -> str:
        if not self.provider:
            logger.error("[Brain] No hay provider disponible")
            return "No hay modelo disponible en este momento."

        start_time = time.time()

        try:
            # ===============================
            # LLM CALL
            # ===============================
            response = await asyncio.wait_for(
                self.provider.generate(prompt),
                timeout=10
            )

            duration = round(time.time() - start_time, 2)

            # ===============================
            # VALIDACIONES DURAS
            # ===============================
            if response is None:
                logger.warning("[Brain] Respuesta None del provider")
                return "No se pudo generar una respuesta."

            if not isinstance(response, str):
                logger.warning(f"[Brain] Tipo inválido: {type(response)}")
                return "Respuesta inválida del modelo."

            response = response.strip()

            if not response:
                logger.warning("[Brain] Respuesta vacía")
                return "No pude generar una respuesta útil."

            # 🔥 Defensa contra respuestas gigantes
            if len(response) > 1000:
                logger.warning("[Brain] Respuesta demasiado larga, recortando")
                response = response[:1000]

            logger.info(f"[Brain] OK ({self.provider_name}) en {duration}s")

            return response

        except asyncio.TimeoutError:
            logger.error(f"[Brain] Timeout ({self.provider_name})")
            return "El modelo está tardando demasiado. Intenta nuevamente."

        except Exception as e:
            logger.error(f"[Brain] Error real ({self.provider_name}): {e}")
            return "Ocurrió un error al generar la respuesta."