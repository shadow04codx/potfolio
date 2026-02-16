"""Pseudo-training script for RL policy used in HE parameter selection."""
import json
import random


def reward(noise, latency, security):
    return -1.5 * noise - latency + 2.0 * security


def main():
    best = None
    for _ in range(1000):
        state = {
            "query_complexity": random.random() * 5,
            "noise": random.random() * 2,
            "latency": random.random() * 1.5,
            "security": random.choice([1, 2, 3]),
        }
        r = reward(state["noise"], state["latency"], state["security"])
        if best is None or r > best["reward"]:
            best = {"state": state, "reward": r}

    with open("ml_training/rl_policy.json", "w", encoding="utf-8") as f:
        json.dump(best, f, indent=2)
    print("Saved mock RL policy to ml_training/rl_policy.json")


if __name__ == "__main__":
    main()
