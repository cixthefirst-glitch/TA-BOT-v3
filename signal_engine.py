from indicators import (
    rsi,
    ema,
    bollinger,
    volume_ratio,
    momentum,
    trend,
)

from smc_engine import analyze

from risk import calculate_trade_levels, passes_rr


def build_signal(symbol, candles):

    closes = [c["close"] for c in candles]
    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]
    volumes = [c["volume"] for c in candles]

    rsi_value = rsi(closes)

    ema20 = ema(closes, 20)
    ema50 = ema(closes, 50)

    upper, middle, lower = bollinger(closes)

    volume = volume_ratio(volumes)

    move = momentum(closes)

    market_trend = trend(closes)

    smc = analyze(candles)

    score = 0

    reasons = []

    side = None

    # ==========================
    # Trend
    # ==========================

    if market_trend == "bullish":
        score += 20
        side = "LONG"

    elif market_trend == "bearish":
        score += 20
        side = "SHORT"

    # ==========================
    # RSI
    # ==========================

    if side == "LONG" and rsi_value < 45:
        score += 10
        reasons.append("Bullish RSI")

    if side == "SHORT" and rsi_value > 55:
        score += 10
        reasons.append("Bearish RSI")

    # ==========================
    # Volume
    # ==========================

    if volume >= 1.5:
        score += 15
        reasons.append("Volume Spike")

    # ==========================
    # Momentum
    # ==========================

    if abs(move) >= 1:
        score += 10
        reasons.append("Strong Momentum")

    # ==========================
    # EMA
    # ==========================

    if ema20 and ema50:

        if side == "LONG" and ema20 > ema50:
            score += 10

        elif side == "SHORT" and ema20 < ema50:
            score += 10

    # ==========================
    # Smart Money Concepts
    # ==========================

    score += smc.structure_strength * 40

    if smc.bos:
        reasons.append("Break Of Structure")

    if smc.choch:
        reasons.append("CHOCH")

    if smc.liquidity_sweep:
        reasons.append("Liquidity Sweep")

    if smc.discount:
        reasons.append("Discount Zone")

    if smc.premium:
        reasons.append("Premium Zone")

    # ==========================
    # Risk
    # ==========================

    levels = calculate_trade_levels(candles, side)

    if not passes_rr(levels):
        return None

    confidence = min(score, 100)

    return {

        "symbol": symbol,

        "side": side,

        "confidence": confidence,

        "entry": levels["entry"],

        "stop": levels["stop"],

        "tp1": levels["tp1"],

        "tp2": levels["tp2"],

        "tp3": levels["tp3"],

        "rr": levels["rr"],

        "atr": levels["atr"],

        "score": score,

        "reasons": reasons,

        "smc": smc.description

    }