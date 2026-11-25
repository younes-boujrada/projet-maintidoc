import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from src.config import GMAO_DB_PATH
from src.security import verify_approval_token
from src.models import TicketRecord


DEFAULT_GMAO_DATA = {
    "equipment": {
        "EPSON-P700-01": {
            "equipment_id": "EPSON-P700-01",
            "model": "Epson SureColor SC-P700",
            "family": "imprimantes_pro",
            "location": "Salle 104 Tirage Fine Art",
            "total_prints": 3850,
            "maintenance_box": "C12C935711",
            "maintenance_box_status": "98% (Saturation imminente - Code 1485)",
            "recent_interventions": [
                {
                    "date": "2026-02-22",
                    "action": "Power Cleaning (Cycle 1)",
                    "technician": "Y. BOUJRADA",
                    "notes": "Banding récurrent sur buses Light Cyan."
                },
                {
                    "date": "2026-02-22",
                    "action": "Power Cleaning (Cycle 2)",
                    "technician": "Y. BOUJRADA",
                    "notes": "Deuxieme purge lourde consecutive. Règle des 12h de repos obligatoire enclenchée."
                }
            ]
        },
        "CANON-R50-LAB01": {
            "equipment_id": "CANON-R50-LAB01",
            "model": "Canon EOS R50",
            "family": "appareils_photo",
            "location": "Studio Plateau B Audiovisuel",
            "shutter_count": 12400,
            "battery_model": "LP-E17",
            "recent_interventions": [
                {
                    "date": "2026-01-15",
                    "action": "Controle annuel & MAJ Firmware v1.1.2",
                    "technician": "M. MALDANI",
                    "notes": "Inspection optique et verification chargeur LC-E17. Aucun voyant critique."
                }
            ]
        }
    },
    "tickets": {}
}


class GMAOMCPServer:
    """
    Model Context Protocol (MCP) Maintenance Service.
    Enforces Point [C3] cryptographic Human-in-the-Loop visa & Idempotency.
    """
    def __init__(self, db_path: str = str(GMAO_DB_PATH)):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        if not os.path.exists(self.db_path):
            self._save_db(DEFAULT_GMAO_DATA)

    def _load_db(self) -> Dict[str, Any]:
        with open(self.db_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_db(self, data: Dict[str, Any]):
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_equipment_history(self, equipment_id: str) -> Dict[str, Any]:
        """Tool MCP : get_equipment_history(equipment_id)"""
        db = self._load_db()
        # Normalization
        target_id = equipment_id.strip().upper()
        if target_id not in db["equipment"]:
            # Check partial match (e.g. 'P700' or 'R50')
            for k in db["equipment"]:
                if target_id in k or k in target_id:
                    target_id = k
                    break

        if target_id in db["equipment"]:
            return {
                "status": "SUCCESS",
                "found": True,
                "data": db["equipment"][target_id]
            }
        return {
            "status": "NOT_FOUND",
            "found": False,
            "message": f"Aucun equipement trouve pour l'identifiant {equipment_id}"
        }

    def create_ticket(
        self,
        equipment_id: str,
        title: str,
        description: str,
        severity: str,
        session_id: str,
        operator_id: str,
        approval_token: str,
        idempotency_key: str,
        recommended_part: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Tool MCP : create_ticket(...)
        Point [C3] Security Verification:
        1. Verifies HMAC-SHA256 human approval visa.
        2. Neutralizes repeated calls via idempotency key.
        """
        # 1. Verify Human-in-the-Loop Cryptographic Visa
        ticket_payload = {
            "equipment_id": equipment_id,
            "title": title,
            "description": description,
            "severity": severity,
            "recommended_part": recommended_part or ""
        }
        
        is_valid_visa = verify_approval_token(
            approval_token,
            session_id=session_id,
            ticket_data=ticket_payload,
            operator_id=operator_id
        )

        if not is_valid_visa:
            return {
                "status": "REJECTED",
                "error": "VIOLATION_POINT_C3",
                "message": (
                    "Action interdite : Aucun jeton d'approbation humaine valide "
                    "(HMAC-SHA256) n'a ete fourni. Le visa de l'operateur est obligatoire."
                )
            }

        db = self._load_db()
        tickets = db.setdefault("tickets", {})

        # 2. Check Idempotency Key (Double-click or network retry protection)
        for tid, tdata in tickets.items():
            if tdata.get("idempotency_key") == idempotency_key:
                return {
                    "status": "SUCCESS",
                    "is_duplicate": True,
                    "ticket_id": tid,
                    "message": "Ticket existant renvoye par cle d'idempotence anti-doublon.",
                    "ticket": tdata
                }

        # 3. Create Ticket Record
        new_id = f"TCK-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        ticket_record = TicketRecord(
            ticket_id=new_id,
            equipment_id=equipment_id,
            title=title,
            description=description,
            severity=severity,
            recommended_part=recommended_part,
            created_at=datetime.now().isoformat(),
            status="OUVERT",
            created_by=operator_id,
            idempotency_key=idempotency_key
        ).model_dump()

        tickets[new_id] = ticket_record
        self._save_db(db)

        return {
            "status": "SUCCESS",
            "is_duplicate": False,
            "ticket_id": new_id,
            "message": "Ticket d'intervention GMAO cree avec succes apres validation humaine.",
            "ticket": ticket_record
        }

    def list_tickets(self, equipment_id: Optional[str] = None) -> List[Dict[str, Any]]:
        db = self._load_db()
        tickets = list(db.get("tickets", {}).values())
        if equipment_id:
            tickets = [t for t in tickets if t.get("equipment_id") == equipment_id]
        return tickets
