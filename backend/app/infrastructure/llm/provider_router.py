# backend/app/infrastructure/llm/provider_router.py
from app.infrastructure.llm.ollama_provider import OllamaProvider
from app.infrastructure.llm.mock_provider import MockProvider

class ProviderRouter:
    """
    Router de proveedores LLM.
    Permite cambiar entre Ollama o Mock fácilmente.
    Preparado para escalar a OpenAI/Gemini en el futuro.
    """
    SUPPORTED_PROVIDERS = {
        "ollama": OllamaProvider,
        "mock": MockProvider,
        # "openai": OpenAIProvider,  # futuro
        # "gemini": GeminiProvider,  # futuro
    }

    def __init__(self, provider_type: str = "ollama"):
        self.provider_type = provider_type.lower()
        self.provider = self._select_provider()

    def _select_provider(self):
        ProviderClass = self.SUPPORTED_PROVIDERS.get(self.provider_type)
        if not ProviderClass:
            raise ValueError(f"Proveedor desconocido: {self.provider_type}. "
                             f"Proveedores soportados: {list(self.SUPPORTED_PROVIDERS.keys())}")
        return ProviderClass()

    def get_provider(self):
        return self.provider