# backend/app/application/use_cases/process_chat.py

from datetime import datetime
import html
import json
import logging
import asyncio
import redis.asyncio as redis

from app.ai_orchestration.brain import Brain
from app.application.dto.chat_dto import ChatRequestDTO, ChatResponseDTO
from app.config.settings import REDIS_URL, MAX_MESSAGE_LENGTH

logger = logging.getLogger("process_chat")

# ===============================
# ⚠️ SpaCy (opcional)
# ===============================
import spacy

try:
    nlp = spacy.load("es_core_news_sm")
except Exception:
    nlp = None
    logger.warning("SpaCy no disponible - análisis emocional desactivado")

# ===============================
# Emociones
# ===============================
EMOTION_KEYWORDS = {
    "malestar": ["estrés","agobiado","preocup","cansado","sobrepasado","ansiedad"],
    "tristeza": ["triste","deprimido","desanimado","melancolía","vacío"],
    "frustracion": ["frustrado","enojado","molesto","irritado","impotencia"],
    "soledad": ["solo","abandono","aislado","desconectado"]
}

def analizar_emocion(msg_text: str):
    if not nlp:
        return []

    try:
        doc = nlp(msg_text.lower())
        tokens = [t.lemma_ for t in doc if not t.is_stop]

        return [
            emo for emo, palabras in EMOTION_KEYWORDS.items()
            if any(p in tokens for p in palabras)
        ]
    except Exception as e:
        logger.error(f"Error en análisis emocional: {e}")
        return []

# ===============================
# Redis
# ===============================
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

HISTORY_LIMIT = 10

async def get_history(user_id: str):
    try:
        raw_msgs = await redis_client.lrange(f"history:{user_id}", -HISTORY_LIMIT, -1)
        return [json.loads(m) for m in raw_msgs]
    except Exception as e:
        logger.error(f"Redis error (get_history): {e}")
        return []

# ===============================
# Prompt
# ===============================
def crear_prompt(history: list, msg_text: str, emociones: list):
    contexto = "\n".join(
        f'{m["userId"]}: {m["content"]}'
        for m in history
    )

    msg_text_safe = html.escape(msg_text)

    return f"""
Eres un asistente de apoyo emocional.

Reglas:
- Sé empático pero NO clínico
- No diagnostiques
- Responde claro, breve y útil
- Máximo 3-4 líneas
- Si detectas emociones, valídalas sin exagerar

Historial:
{contexto}

Usuario:
{msg_text_safe}

Emociones detectadas:
{emociones}

Respuesta:
"""

# ===============================
# Use Case
# ===============================
class ProcessChatUseCase:
    def __init__(self, llm_provider=None):
        self.brain = Brain(llm_provider=llm_provider)

    async def execute(self, request: ChatRequestDTO) -> ChatResponseDTO:
        msg_text = request.message[:MAX_MESSAGE_LENGTH]

        logger.info(f"Mensaje recibido: {msg_text}")

        # ===============================
        # Emoción + historial
        # ===============================
        emociones = analizar_emocion(msg_text)
        history = await get_history(request.user_id)

        prompt = crear_prompt(history, msg_text, emociones)

        logger.info(f"Prompt generado (resumen): {prompt[:200]}...")

        # ===============================
        # LLM protegido
        # ===============================
        try:
            ai_response = await asyncio.wait_for(
                self.brain.think(prompt),
                timeout=12
            )
        except asyncio.TimeoutError:
            logger.error("Timeout LLM")
            ai_response = "Estoy tardando más de lo esperado. Intenta nuevamente."
        except Exception as e:
            logger.error(f"Error LLM: {e}")
            ai_response = "Ocurrió un error generando la respuesta."

        logger.info(f"Respuesta generada: {ai_response}")

        # ===============================
        # Persistencia Redis (segura)
        # ===============================
        timestamp = datetime.utcnow().isoformat()

        try:
            await redis_client.rpush(
                f"history:{request.user_id}",
                json.dumps({
                    "userId": request.user_id,
                    "content": msg_text,
                    "isUser": True,
                    "createdAt": timestamp
                })
            )

            await redis_client.rpush(
                f"history:{request.user_id}",
                json.dumps({
                    "userId": "neurochat",
                    "content": ai_response,
                    "isUser": False,
                    "createdAt": timestamp
                })
            )

            await redis_client.ltrim(f"history:{request.user_id}", -HISTORY_LIMIT, -1)
            await redis_client.expire(f"history:{request.user_id}", 3600)

        except Exception as e:
            logger.error(f"Redis error (persistencia): {e}")

        return ChatResponseDTO(response=ai_response)