from typing import Dict
from time import perf_counter
from backend.encryption.he_engine import HomomorphicEncryptionEngine


class BenchmarkService:
    def __init__(self, he: HomomorphicEncryptionEngine):
        self.he = he

    def run(self) -> Dict:
        values = [1.0, 2.0, 3.0, 4.0]
        start = perf_counter()
        c1 = self.he.encrypt(values)
        enc_time = perf_counter() - start

        start = perf_counter()
        _ = self.he.add(c1.ciphertext, c1.ciphertext, c1.context_blob)
        add_time = perf_counter() - start

        start = perf_counter()
        _ = self.he.multiply(c1.ciphertext, c1.ciphertext, c1.context_blob)
        mul_time = perf_counter() - start

        return {
            "encrypt_ms": round(enc_time * 1000, 4),
            "add_ms": round(add_time * 1000, 4),
            "mul_ms": round(mul_time * 1000, 4),
            "noise_growth_simulated": round((add_time + mul_time) * 100, 6),
        }
