import json
import math
from pathlib import Path

MODEL_FILE = Path("data/model_coefs.json")


def _sigmoid(x):
    return 1 / (1 + math.exp(-x))


def predict_probability(features):
    if not MODEL_FILE.exists():
        return 0.5

    with open(MODEL_FILE, "r") as f:
        model = json.load(f)

    coefs = model.get("coefs", {})
    intercept = model.get("intercept", 0)

    score = intercept

    for key, value in features.items():
        if key in coefs:
            score += value * coefs[key]

    return _sigmoid(score)
