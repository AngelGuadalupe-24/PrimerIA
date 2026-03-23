# backend/app/interface/websocket/neurochat_socket.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from datetime import datetime
from typing import Dict, List
import logging
import asyncio
import json

router = APIRouter(prefix="/ws/neurochat")

logger = logging.getLogger("neurochat_ws")
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

logger.info("🔥 WEBSOCKET FILE CARGADO")


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        async with self.lock:
            if user_id not in self.active_connections:
                self.active_connections[user_id] = []
            self.active_connections[user_id].append(websocket)
        logger.info(f"🟢 Conectado: {user_id}")

    async def disconnect(self, websocket: WebSocket, user_id: str):
        async with self.lock:
            if user_id in self.active_connections:
                if websocket in self.active_connections[user_id]:
                    self.active_connections[user_id].remove(websocket)
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]
        logger.info(f"🔴 Desconectado: {user_id}")

    async def send_message(self, message: dict, user_id: str):
        async with self.lock:
            connections = self.active_connections.get(user_id, []).copy()

        for ws in connections:
            try:
                await ws.send_json(message)
            except Exception as e:
                logger.warning(f"❌ Falló envío a {user_id}, eliminando conexión: {e}")
                await self.disconnect(ws, user_id)


manager = ConnectionManager()


@router.websocket("/{user_id}")
async def neurochat_ws(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)

    try:
        while True:
            try:
                raw_data = await websocket.receive_text()
                try:
                    data = json.loads(raw_data)
                    msg_type = data.get("type", "message")
                    content = data.get("content", "")
                except json.JSONDecodeError:
                    logger.warning(f"⚠️ JSON inválido de {user_id}: {raw_data}")
                    content = raw_data
                    msg_type = "message"

                logger.info(f"📩 {user_id} ({msg_type}): {content}")

                # Construir respuesta según tipo
                response = {
                    "id": int(datetime.utcnow().timestamp() * 1000),
                    "userId": "neurochat",
                    "content": f"Echo ({msg_type}): {content}",
                    "type": msg_type,
                    "isUser": False,
                    "createdAt": datetime.utcnow().isoformat()
                }

                await manager.send_message(response, user_id)

            except WebSocketDisconnect:
                await manager.disconnect(websocket, user_id)
                break

            except Exception as e:
                logger.error(f"🔥 Error recibiendo mensaje de {user_id}: {e}")
                await manager.disconnect(websocket, user_id)
                break

    except Exception as e:
        logger.error(f"🔥 Error general WS {user_id}: {e}")
        await manager.disconnect(websocket, user_id)