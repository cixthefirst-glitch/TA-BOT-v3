from scanner import scan_market
from signal_engine import build_signal
from gemini_ai import ask_gemini
from telegram_bot import send_message, format_signal
from tracker import add_signal, open_signals
from learning import record_trade
from utils import log


def scan():
    log("Scanning market...")

    market = scan_market()

    signals = []

    for coin in market:

        signal = build_signal(
            coin["symbol"],
            coin["candles"]
        )

        if signal is None:
            continue

        approved, reply = ask_gemini(signal)

        signal["gemini"] = reply

        if not approved:
            continue

        add_signal(signal)

        send_message(
            format_signal(signal)
        )

        signals.append(signal)

    log(f"{len(signals)} signals sent.")


if __name__ == "__main__":
    scan()