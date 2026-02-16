from dataclasses import dataclass
import torch
import torch.nn as nn


class NoiseRegressor(nn.Module):
    def __init__(self, in_dim: int = 4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
        )

    def forward(self, x):
        return self.net(x)


@dataclass
class NoisePredictionService:
    model: NoiseRegressor

    @classmethod
    def with_default_weights(cls):
        model = NoiseRegressor()
        model.eval()
        return cls(model)

    def predict(self, features):
        x = torch.tensor([features], dtype=torch.float32)
        with torch.no_grad():
            return float(self.model(x).item())
