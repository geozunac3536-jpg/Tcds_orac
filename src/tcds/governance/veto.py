from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Any

@dataclass
class Decision:
    event_id: str
    decision: str  # "PASS", "FAIL", "HOLD"
    reason: str
    metrics: Dict[str, float]
    bias_applied: float
    timestamp: str

class OmnipresentVeto:
    """
    Implementa el E-Veto (Veto Entrópico).
    Aplica umbrales rígidos de Sigma-Metrics modulados por un sesgo cognitivo.
    """
    def __init__(self):
        # KPIs Base (Configuración 'Hardcoded' por defecto)
        self.LI_MIN = 0.90
        self.R_MIN = 0.95
        self.RMSE_MAX = 0.10
        self.DH_MAX = -0.20  # La caída de entropía requerida

    def judge(self, packet: Dict[str, Any], bias: float = 0.0) -> Decision:
        """
        Evalúa un paquete de datos.
        bias: Valor positivo relaja el veto, negativo lo endurece.
        """
        # 1. Extraer métricas (con valores default seguros)
        ev_id = str(packet.get("event_id", "UNKNOWN"))
        li = float(packet.get("LI", 0.0))
        r = float(packet.get("R", 0.0))
        rmse = float(packet.get("RMSE_SL", 1.0))
        dh = float(packet.get("dH", 0.0))

        # 2. Ajustar el E-Veto con el Bias Cognitivo (Simbiosis)
        # Un bias positivo hace que el DH_MAX sea menos negativo (más fácil de pasar)
        # Un bias negativo hace que sea más negativo (más difícil)
        effective_dh_threshold = self.DH_MAX + bias

        # 3. Evaluar consistencia matemática (Sigma)
        sigma_pass = (li >= self.LI_MIN) and (r >= self.R_MIN) and (rmse <= self.RMSE_MAX)

        # 4. Evaluar diseño entrópico
        entropy_pass = (dh <= effective_dh_threshold)

        # 5. Emitir Veredicto
        if sigma_pass and entropy_pass:
            decision = "PASS"
            reason = f"Validado. Sigma OK. dH({dh:.3f}) <= Umbral({effective_dh_threshold:.3f})"
        elif sigma_pass and not entropy_pass:
            decision = "FAIL"
            reason = f"Rechazo Entrópico. dH({dh:.3f}) > Umbral({effective_dh_threshold:.3f})"
        else:
            decision = "HOLD"
            reason = "Fallo en métricas Sigma (Inconsistencia matemática)."

        return Decision(
            event_id=ev_id,
            decision=decision,
            reason=reason,
            metrics={"LI": li, "R": r, "RMSE": rmse, "dH": dh},
            bias_applied=bias,
            timestamp=datetime.now(timezone.utc).isoformat()
        )