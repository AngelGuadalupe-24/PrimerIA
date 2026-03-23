# ai_orchestration/agents/safety_agent.py

class SafetyAgent:

    def is_risky(self, message: str) -> bool:
        keywords = ["suicidio", "matarme", "no quiero vivir"]
        return any(word in message.lower() for word in keywords)

    def crisis_response(self) -> str:
        return "Si estás en peligro inmediato, por favor busca ayuda profesional o contacta un servicio de emergencia en tu país."