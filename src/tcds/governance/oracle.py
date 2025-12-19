import time
import json
from ..cognitive.memory import ReasoningEngine
from ..cognitive.analyzer import LinguisticAnalyzer
from .veto import OmnipresentVeto
from .io import OracleIO

class CognitiveOracle:
    """
    La entidad principal. Une el Cerebro (Cognitive) con el Juez (Veto).
    """
    def __init__(self, data_root="./tcds_data"):
        # 1. Inicializar Cerebro (MUSE)
        self.analyzer = LinguisticAnalyzer()
        self.brain = ReasoningEngine(self.analyzer)

        # 2. Inicializar Juez y IO
        self.veto = OmnipresentVeto()
        self.io = OracleIO(data_root)

        print("👁️ ORACLE: Sistema inicializado. Simbiosis activa.")

    def _calculate_cognitive_bias(self, packet: dict) -> float:
        """
        El 'CognitiveBridge': Traduce el estado emocional a un bias numérico.
        """
        # Analizar metadatos o texto del paquete si existe
        text_content = packet.get("meta_text", "") or "sys_event"

        # El cerebro 'ingiere' el evento superficialmente para actualizar emociones
        self.brain.ingest_knowledge(text_content, label="event_scan")

        state = self.brain.emotional_state

        bias = 0.0
        # Regla 1: Alta confianza relaja el veto (+0.05)
        if state.confianza > 0.8:
            bias += 0.05

        # Regla 2: Alta fatiga endurece el veto (-0.05) - Modo "Gruñón"
        if state.fatiga > 0.7:
            bias -= 0.05

        # Regla 3: Si la coherencia interna del sistema baja, bloqueo total (-0.2)
        if state.coherencia < 0.5:
            bias -= 0.2

        return bias

    def process_one_cycle(self):
        """Procesa todos los archivos en el inbox"""
        pending_files = self.io.scan_inbox()

        if not pending_files:
            return "IDLE"

        results = []
        for file_path in pending_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    packet = json.load(f)

                # A. Calcular Sesgo (La parte humana/cognitiva)
                bias = self._calculate_cognitive_bias(packet)

                # B. Juzgar (La parte determinista matemática)
                verdict = self.veto.judge(packet, bias=bias)

                # C. Escribir resultado
                out_path = self.io.write_decision(verdict)

                # D. Archivar
                self.io.archive_packet(file_path)

                results.append(f"{verdict.event_id}: {verdict.decision}")

            except Exception as e:
                print(f"❌ Error procesando {file_path}: {e}")

        return results