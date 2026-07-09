import math


def rsi(closes, period=14):
    if len(closes) < period + 1:
        return 50

    gains = []
    losses = []

    for i in range(1, len(closes)):
        change = closes[i] - closes[i - 1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def ema(data, period):
    if len(data) < period:
        return None

    multiplier = 2 / (period + 1)

    value = sum(data[:period]) / period

    for price in data[period:]:
        value = (price - value) * multiplier + value

    return value


def sma(data, period):
    if len(data) < period:
        return None

    return sum(data[-period:]) / period


def bollinger(closes, period=20, std=2):
    if len(closes) < period:
        return None, None, None

    middle = sma(closes, period)

    variance = sum((x - middle) ** 2 for x in closes[-period:]) / period

    deviation = math.sqrt(variance)

    upper = middle + std * deviation
    lower = middle - std * deviation

    return upper, middle, lower


def atr(highs, lows, closes, period=14):
    if len(highs) < period + 1:
        return None

    tr = []

    for i in range(1, len(highs)):
        tr.append(max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1])
        ))

    return sum(tr[-period:]) / period


def volume_ratio(volumes, period=20):
    if len(volumes) < period:
        return 1.0

    average = sum(volumes[-period:]) / period

    if average == 0:
        return 1.0

    return volumes[-1] / average


def momentum(closes, candles=1):
    if len(closes) <= candles:
        return 0

    return ((closes[-1] - closes[-1 - candles]) / closes[-1 - candles