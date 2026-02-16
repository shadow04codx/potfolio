from dataclasses import dataclass
from typing import Dict
import random


@dataclass
class RLOptimizerService:
    """Heuristic DQN-like policy stub with production-friendly interface."""

    candidate_params = [
        {"lambda": 128, "poly_modulus_degree": 8192, "coeff_modulus": [60, 40, 40, 60]},
        {"lambda": 192, "poly_modulus_degree": 16384, "coeff_modulus": [60, 40, 40, 40, 60]},
        {"lambda": 256, "poly_modulus_degree": 32768, "coeff_modulus": [60, 50, 40, 40, 40, 60]},
    ]

    def recommend(self, query_complexity: float, predicted_noise: float) -> Dict:
        if query_complexity > 4 or predicted_noise > 1.2:
            idx = 2
        elif query_complexity > 2:
            idx = 1
        else:
            idx = 0

        params = dict(self.candidate_params[idx])
        params["policy_confidence"] = round(0.82 + random.random() * 0.15, 3)
        return params
