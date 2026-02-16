"""Train lightweight query optimizer model with synthetic query features."""
import torch
import torch.nn as nn
import torch.optim as optim
from backend.ml_models.gnn_query_optimizer import SimpleQueryGNN


def main():
    model = SimpleQueryGNN()
    X = torch.rand((800, 6)) * 10
    y_depth = (X[:, 0] * 0.12 + X[:, 1] * 0.8 + X[:, 4] * 0.4).unsqueeze(1)
    y_noise = (X[:, 2] * 0.5 + X[:, 3] * 0.6 + X[:, 5] * 0.3).unsqueeze(1)

    opt = optim.Adam(model.parameters(), lr=1e-3)
    mse = nn.MSELoss()

    for _ in range(250):
        depth, noise = model(X)
        loss = mse(depth, y_depth) + mse(noise, y_noise)
        opt.zero_grad()
        loss.backward()
        opt.step()

    torch.save(model.state_dict(), "ml_training/query_gnn.pt")
    print("Saved query GNN to ml_training/query_gnn.pt")


if __name__ == "__main__":
    main()
