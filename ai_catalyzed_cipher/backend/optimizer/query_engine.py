import time
from typing import Dict, List
from sqlalchemy.orm import Session
from backend.database.models import EncryptedRecord
from backend.encryption.he_engine import HomomorphicEncryptionEngine


class SecureQueryEngine:
    def __init__(self, he_engine: HomomorphicEncryptionEngine):
        self.he = he_engine

    def execute(self, db: Session, record_ids: List[int], operation: str, vector=None) -> Dict:
        started = time.time()
        rows = db.query(EncryptedRecord).filter(EncryptedRecord.id.in_(record_ids)).all()
        if not rows:
            raise ValueError("No matching encrypted records")

        context = rows[0].context_blob
        ciphertexts = [r.ciphertext for r in rows]

        agg = ciphertexts[0]
        for c in ciphertexts[1:]:
            agg = self.he.add(agg, c, context)

        if operation == "mean":
            plain = self.he.decrypt(agg, context)
            plain = [v / len(ciphertexts) for v in plain]
            agg = self.he.encrypt(plain).ciphertext
        elif operation == "dot":
            if not vector:
                raise ValueError("vector is required for dot operation")
            vec_cipher = self.he.encrypt(vector)
            agg = self.he.multiply(agg, vec_cipher.ciphertext, context)

        decrypted = self.he.decrypt(agg, context)
        elapsed = time.time() - started

        return {
            "encrypted_result": agg,
            "decrypted_result": decrypted,
            "metadata": {
                "record_count": len(rows),
                "operation": operation,
                "latency_ms": round(elapsed * 1000, 2),
                "noise_budget_estimate": round(max(0.0, 1.0 - elapsed / 5), 4),
            },
        }
