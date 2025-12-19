from datetime import datetime, timezone
from .emotions import EmotionalState

class ReasoningEngine:
    """Motor de razonamiento y gestión de estado emocional"""
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.emotional_state = EmotionalState(
            confianza=0.5,
            vigilancia=0.7,
            fatiga=0.0,
            coherencia=1.0,
            legado=0.0,
            timestamp=datetime.now(timezone.utc)
        )
        self.knowledge_base = []

    def ingest_knowledge(self, text: str, label: str):
        self.emotional_state.vigilancia = min(1.0, self.emotional_state.vigilancia + 0.01)
        if "error" in text.lower() or "fallo" in text.lower():
            self.emotional_state.confianza = max(0.0, self.emotional_state.confianza - 0.1)
            self.emotional_state.fatiga += 0.05
        else:
            self.emotional_state.confianza = min(1.0, self.emotional_state.confianza + 0.05)
        return {"status": "ingested", "label": label}