def extract_features(indicators, side):
    smc = indicators.get("smc", {})

    return {
        "rsi": indicators.get("rsi", 50),
        "volume_ratio": indicators.get("volume_ratio", 1.0),
        "momentum_1h": indicators.get("momentum_1h", 0),
        "score": indicators.get("score", 0.5),
        "btc_24h": indicators.get("btc_24h", 0),

        "structure_strength": smc.get("structure_strength", 0.0),
        "in_discount": float(smc.get("in_discount", False)),
        "in_premium": float(smc.get("in_premium", False)),
        "near_supply_zone": float(smc.get("near_supply_zone", False)),
        "near_demand_zone": float(smc.get("near_demand_zone", False)),
        "choch_recently": float(smc.get("choch_recently", False)),

        "side_long": float(side == "LONG"),
    }
