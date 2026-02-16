from dataclasses import dataclass
from typing import Dict
import torch
import torch.nn as nn


class SimpleQueryGNN(nn.Module):
    """Lightweight graph-like encoder for query token statistics."""

    def __init__(self, input_dim=6, hidden_dim=32):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
        )
        self.depth_head = nn.Linear(hidden_dim, 1)
        self.noise_head = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        h = self.encoder(x)
        return self.depth_head(h), self.noise_head(h)


@dataclass
class QueryOptimizationService:
    model: SimpleQueryGNN

    @classmethod
    def build(cls):
        model = SimpleQueryGNN()
        model.eval()
        return cls(model=model)

    def featurize_query(self, sql: str):
        sql_l = sql.lower()
        tokens = sql_l.split()
        return [
            len(tokens),
            sql_l.count("join"),
            sql_l.count("where"),
            sql_l.count("sum") + sql_l.count("avg"),
            sql_l.count("*") + sql_l.count("/") + sql_l.count("-"),
            sql_l.count("group by"),
        ]

    def optimize(self, sql: str) -> Dict:
        feats = self.featurize_query(sql)
        x = torch.tensor([feats], dtype=torch.float32)
        with torch.no_grad():
            depth, noise = self.model(x)

        multiplicative_depth = max(1.0, float(depth.item()) + 3.0)
        noise_growth = max(0.01, float(noise.item()) + 0.5)

        return {
            "multiplicative_depth": multiplicative_depth,
            "predicted_noise_growth": noise_growth,
            "optimized_plan": {
                "rewrite": "Push filters before multiplications and aggregate late",
                "execution_stages": ["scan", "filter", "he-eval", "aggregate"],
                "token_features": feats,
            },
        }
