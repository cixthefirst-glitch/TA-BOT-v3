from dataclasses import dataclass


@dataclass
class SMCResult:

    trend: str

    bos: bool

    choch: bool

    liquidity_sweep: bool

    premium: bool

    discount: bool

    structure_strength: float

    description: str


def highest_high(candles, length=20):

    return max(c["high"] for c in candles[-length:])


def lowest_low(candles, length=20):

    return min(c["low"] for c in candles[-length:])


def detect_trend(candles):

    if len(candles) < 30:

        return "neutral"

    highs = [c["high"] for c in candles[-10:]]

    lows = [c["low"] for c in candles[-10:]]

    if highs[-1] > highs[0] and lows[-1] > lows[0]:

        return "bullish"

    if highs[-1] < highs[0] and lows[-1] < lows[0]:

        return "bearish"

    return "neutral"


def detect_bos(candles):

    if len(candles) < 25:

        return False

    previous_high = highest_high(candles[:-1],20)

    previous_low = lowest_low(candles[:-1],20)

    close = candles[-1]["close"]

    return close > previous_high or close < previous_low


def detect_choch(candles):

    if len(candles) < 35:

        return False

    trend = detect_trend(candles)

    close = candles[-1]["close"]

    prev = candles[-6]["close"]

    if trend == "bullish" and close < prev:

        return True

    if trend == "bearish" and close > prev:

        return True

    return False


def detect_liquidity_sweep(candles):

    if len(candles) < 15:

        return False

    last = candles[-1]

    previous_high = highest_high(candles[:-1],10)

    previous_low = lowest_low(candles[:-1],10)

    if last["high"] > previous_high and last["close"] < previous_high:

        return True

    if last["low"] < previous_low and last["close"] > previous_low:

        return True

    return False


def premium_discount(candles):

    high = highest_high(candles,50)

    low = lowest_low(candles,50)

    mid = (high + low)/2

    price = candles[-1]["close"]

    return price > mid, price < mid


def analyze(candles):

    trend = detect_trend(candles)

    bos = detect_bos(candles)

    choch = detect_choch(candles)

    sweep = detect_liquidity_sweep(candles)

    premium, discount = premium_discount(candles)

    strength = 0

    if bos:

        strength += 0.4

    if choch:

        strength += 0.3

    if sweep:

        strength += 0.2

    if trend != "neutral":

        strength += 0.1

    desc = []

    if bos:

        desc.append("BOS")

    if choch:

        desc.append("CHoCH")

    if sweep:

        desc.append("Liquidity Sweep")

    if premium:

        desc.append("Premium")

    if discount:

        desc.append("Discount")

    return SMCResult(

        trend,

        bos,

        choch,

        sweep,

        premium,

        discount,

        strength,

        " | ".join(desc)

    )