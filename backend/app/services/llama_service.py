# backend/app/services/llama_service.py

def llama_respond(prompt: str) -> str:
    """
    Esta función recibe un texto del usuario y devuelve
    la respuesta del modelo LLaMA.

    Por ahora hacemos un mock simple; luego reemplaza
    con la lógica real de LLaMA (API local, llama.cpp o similar)
    """
    # MOCK: responde con lo que recibió (simulación)
    # placeholder temporal
    # Aquí luego llamaremos a LLaMA real
    return f"LLaMA dice: {prompt[::-1]}"  # ejemplo: devuelve el texto invertido