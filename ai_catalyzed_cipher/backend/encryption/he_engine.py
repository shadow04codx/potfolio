import base64
import json
from dataclasses import dataclass
from typing import List

try:
    import tenseal as ts
except Exception:  # optional dependency fallback
    ts = None


@dataclass
class CipherPackage:
    ciphertext: str
    context_blob: str


class HomomorphicEncryptionEngine:
    """TenSEAL-backed CKKS engine with a deterministic JSON fallback for local dev."""

    def __init__(self):
        self.poly_modulus_degree = 8192
        self.coeff_mod_bit_sizes = [60, 40, 40, 60]
        self.global_scale = 2**40

    def _build_context(self):
        context = ts.context(
            ts.SCHEME_TYPE.CKKS,
            poly_modulus_degree=self.poly_modulus_degree,
            coeff_mod_bit_sizes=self.coeff_mod_bit_sizes,
        )
        context.global_scale = self.global_scale
        context.generate_galois_keys()
        return context

    def encrypt(self, values: List[float]) -> CipherPackage:
        if ts is None:
            blob = base64.b64encode(json.dumps(values).encode()).decode()
            return CipherPackage(ciphertext=blob, context_blob="fallback")

        context = self._build_context()
        enc = ts.ckks_vector(context, values)
        ctxt = base64.b64encode(enc.serialize()).decode()
        ctx = base64.b64encode(context.serialize(save_secret_key=True)).decode()
        return CipherPackage(ciphertext=ctxt, context_blob=ctx)

    def decrypt(self, ciphertext: str, context_blob: str) -> List[float]:
        if context_blob == "fallback" or ts is None:
            return json.loads(base64.b64decode(ciphertext.encode()).decode())

        context = ts.context_from(base64.b64decode(context_blob.encode()))
        enc = ts.ckks_vector_from(context, base64.b64decode(ciphertext.encode()))
        return [float(v) for v in enc.decrypt()]

    def add(self, lhs: str, rhs: str, context_blob: str) -> str:
        if context_blob == "fallback" or ts is None:
            l = json.loads(base64.b64decode(lhs.encode()).decode())
            r = json.loads(base64.b64decode(rhs.encode()).decode())
            out = [a + b for a, b in zip(l, r)]
            return base64.b64encode(json.dumps(out).encode()).decode()

        context = ts.context_from(base64.b64decode(context_blob.encode()))
        l_enc = ts.ckks_vector_from(context, base64.b64decode(lhs.encode()))
        r_enc = ts.ckks_vector_from(context, base64.b64decode(rhs.encode()))
        l_enc += r_enc
        return base64.b64encode(l_enc.serialize()).decode()

    def multiply(self, lhs: str, rhs: str, context_blob: str) -> str:
        if context_blob == "fallback" or ts is None:
            l = json.loads(base64.b64decode(lhs.encode()).decode())
            r = json.loads(base64.b64decode(rhs.encode()).decode())
            out = [a * b for a, b in zip(l, r)]
            return base64.b64encode(json.dumps(out).encode()).decode()

        context = ts.context_from(base64.b64decode(context_blob.encode()))
        l_enc = ts.ckks_vector_from(context, base64.b64decode(lhs.encode()))
        r_enc = ts.ckks_vector_from(context, base64.b64decode(rhs.encode()))
        l_enc *= r_enc
        return base64.b64encode(l_enc.serialize()).decode()
