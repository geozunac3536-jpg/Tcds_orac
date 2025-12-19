import os
import json
import glob
import uuid
import time

class OracleIO:
    """Manejo de archivos para el Oráculo (Inboxes/Outboxes)"""

    def __init__(self, root_dir: str = "./oracle_data"):
        self.inbox = os.path.join(root_dir, "inbox")
        self.outbox = os.path.join(root_dir, "outbox_decisions")
        self.archive = os.path.join(root_dir, "archive")

        for d in [self.inbox, self.outbox, self.archive]:
            os.makedirs(d, exist_ok=True)

    def scan_inbox(self):
        """Busca archivos JSON pendientes"""
        return glob.glob(os.path.join(self.inbox, "*.json"))

    def write_decision(self, decision_obj):
        """Escritura atómica de la decisión"""
        filename = f"DECISION_{decision_obj.event_id}.json"
        path = os.path.join(self.outbox, filename)

        # Convertir dataclass a dict
        data = decision_obj.__dict__

        tmp = path + f".tmp.{uuid.uuid4().hex}"
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        os.replace(tmp, path)
        return path

    def archive_packet(self, file_path):
        """Mueve el paquete procesado al archivo"""
        filename = os.path.basename(file_path)
        dest = os.path.join(self.archive, filename)
        os.replace(file_path, dest)