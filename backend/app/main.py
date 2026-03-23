from fastapi import FastAPI

print("🔥 MAIN CORRECTO CARGADO")

# HTTP
from app.interface.http.chat_controller import router as chat_router

# WebSocket (ÚNICO)
from app.interface.websocket.neurochat_socket import router as neurochat_ws_router

app = FastAPI(
    title="PrimerIA Backend",
    version="1.0.0"
)

# =========================
# HTTP ROUTES
# =========================
app.include_router(chat_router)

# =========================
# WEBSOCKET ROUTES
# =========================
app.include_router(neurochat_ws_router)


# 🔴 AGREGA ESTO
for route in app.routes:
    if hasattr(route, "methods"):  # Solo las HTTP
        print("👉", route.path, route.name, route.methods)
    else:  # WebSocket u otros
        print("👉", route.path, route.name, type(route))

# =========================
# HEALTH CHECK
# =========================

@app.get("/")
async def root():
    return {"status": "ok", "message": "Backend activo"}