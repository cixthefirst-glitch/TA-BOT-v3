from indicators import atr
from config import ATR_SL_MULTIPLIER, MIN_RR


def calculate_trade_levels(candles, side):
    """
    Calculate Entry, Stop Loss, Take Profits and Risk:Reward
    using ATR.
    """

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]
    closes = [c["close"] for c in candles]

    entry = closes[-1]

    atr_value = atr(highs, lows, closes)

    if atr_value is None:
        return None

    risk = atr_value * ATR_SL_MULTIPLIER

    if side == "LONG":

        stop = entry - risk

        tp1 = entry + risk
        tp2 = entry + (risk * 2)
        tp3 = entry + (risk * 3)

    else:

        stop = entry + risk

        tp1 = entry - risk
        tp2 = entry - (risk * 2)
        tp3 = entry - (risk * 3)

    rr = abs(tp3 - entry) / abs(entry - stop)

    return {
        "entry": entry,
        "stop": stop,
        "tp1": tp1,
        "tp2": tp2,
        "tp3": tp3,
        "rr": rr,
        "atr": atr_value
    }


def passes_rr(levels):
    """
    Reject trades with poor Risk:Reward.
    """

    if levels is None:
        return False

    return levels["rr"] >= MIN_RR


def move_stop_to_breakeven(signal):
    """
    Move stop loss to entry after TP1.
    """

    signal["stop"] = signal["entry"]

    return signal


def trailing_stop(signal, current_price):
    """
    Simple ATR-based trailing stop.
    """

    atr_value = signal.get("atr")

    if atr_value is None:
        return signal

    if signal["side"] == "LONG":

        new_stop = current_price - atr_value

        if new_stop > signal["stop"]:
            signal["stop"] = new_stop

    else:

        new_stop = current_price + atr_value

        if new_stop < signal["stop"]:
            signal["stop"] = new_stop

    return signal