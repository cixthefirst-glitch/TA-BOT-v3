import os
import json

DATASET_FILE = "data/training_data.json"


def load_dataset():
    if not os.path.exists(DATASET_FILE):
        return []

    with open(DATASET_FILE, "r") as f:
        return json.load(f)


def save_dataset(data):

    os.makedirs("data", exist_ok=True)

    with open(DATASET_FILE, "w") as f:
        json.dump(data, f, indent=4)


def record_trade(signal, outcome):
    """
    outcome:
        1 = WIN
        0 = LOSS
    """

    dataset = load_dataset()

    dataset.append({

        "symbol": signal["symbol"],

        "side": signal["side"],

        "confidence": signal["confidence"],

        "rr": signal["rr"],

        "score": signal["score"],

        "reasons": signal["reasons"],

        "outcome": outcome

    })

    save_dataset(dataset)


def win_rate():

    dataset = load_dataset()

    if not dataset:
        return 0

    wins = sum(x["outcome"] for x in dataset)

    return round((wins / len(dataset)) * 100, 2)


def total_trades():

    return len(load_dataset())


def stats():

    return {

        "total": total_trades(),

        "win_rate": win_rate()

    }