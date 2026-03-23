import os

# Tipo de proveedor de LLM por defecto: "ollama", "mock", "openai", "gemini", etc.
PROVIDER_TYPE = os.getenv("PROVIDER_TYPE", "ollama")

# Redis URL
# Por defecto apunta a localhost (Windows), pero si hay variable de entorno REDIS_URL, la usa (Docker/Linux)
REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379")

# Longitud máxima de mensaje permitido al LLM
MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", 2000))

# Número máximo de conexiones concurrentes (para semáforos, sockets, etc.)
MAX_CONNECTIONS = int(os.getenv("MAX_CONNECTIONS", 5))

# Otros settings que puedas necesitar en el futuro
# CACHE_EXPIRE_SECONDS = int(os.getenv("CACHE_EXPIRE_SECONDS", 3600))