"""Train a noise regression model for HE noise growth estimation."""
import torch
import torch.nn as nn
import torch.optim as optim
from backend.ml_models.noise_model import NoiseRegressor


def main():
    model = NoiseRegressor()
    X = torch.rand((500, 4))
    y = (0.5 * X[:, 0] + 0.3 * X[:, 1] + 0.2 * X[:, 3]).unsqueeze(1)

    loss_fn = nn.MSELoss()
    opt = optim.Adam(model.parameters(), lr=1e-3)

    for _ in range(200):
        pred = model(X)
        loss = loss_fn(pred, y)
        opt.zero_grad()
        loss.backward()
        opt.step()

    torch.save(model.state_dict(), "ml_training/noise_model.pt")
    print("Saved noise model to ml_training/noise_model.pt")


if __name__ == "__main__":
    main()
