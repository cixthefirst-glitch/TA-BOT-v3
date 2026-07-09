import json
import os

SIGNALS_FILE = "data/signals.json"


def load_signals():
    if not os.path.exists(SIGNALS_FILE):
        return []

    with open(SIGNALS_FILE, "r") as f:
        return json.load(f)


def save_signals(signals):

    os.makedirs("data", exist_ok=True)

    with open(SIGNALS_FILE, "w") as f:
        json.dump(signals, f, indent=4)


def add_signal(signal):

    signals = load_signals()

    signals.append(signal)

    save_signals(signals)


def update_signal(symbol, status):

    signals = load_signals()

    for signal in signals:

        if signal["symbol"] == symbol and signal.get("status") == "OPEN":

            signal["status"] = status

    save_signals(signals)


def open_signals():

    return [

        s

        for s in load_signals()

        if s.get("status") == "OPEN"

    ]