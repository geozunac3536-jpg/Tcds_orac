from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class EmotionalValence(Enum):
    MUY_POSITIVA = 2
    POSITIVA = 1
    NEUTRA = 0
    NEGATIVA = -1
    MUY_NEGATIVA = -2

@dataclass
class EmotionalState:
    confianza: float      # [0,1]
    vigilancia: float     # [0,1]
    fatiga: float         # [0,1]
    coherencia: float     # [0,1]
    legado: float         # [0,1]
    timestamp: datetime

    def compute_mood(self) -> str:
        score = (
            self.confianza * 0.3 +
            self.vigilancia * 0.2 +
            (1 - self.fatiga) * 0.2 +
            self.coherencia * 0.2 +
            self.legado * 0.1
        )
        if score > 0.8: return "ÓPTIMO"
        elif score > 0.6: return "VIGILANTE"
        elif score > 0.4: return "CAUTELOSO"
        elif score > 0.2: return "ESTRESADO"
        else: return "DEGRADADO"