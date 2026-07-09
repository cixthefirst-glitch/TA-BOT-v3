import requests
from concurrent.futures import ThreadPoolExecutor

from config import FUTURES_BASE, TOP_COINS, MAX_WORKERS

_INTERVAL_MAP = {
    "1m": "Min1",
    "5m": "Min5",
    "15m": "Min15",
    "30m": "Min30",
    "60m": "Min60",
    "4h": "Hour4",
    "1d": "Day1",
}


def get_perpetual_symbols():
    url = f"{FUTURES_BASE}/api/v1/contract/detail"

    try:
        r = requests.get(url, timeout=15)
        data = r.json()["data"]

        symbols = []

        for coin in data:
            if (
                coin["symbol"].endswith("_USDT")
                and coin["settleCoin"] == "USDT"
                and coin["deliveryDate"] == 0
            ):
                symbols.append(coin["symbol"])

        return symbols

    except Exception as e:
        print(e)
        return []


def get_top_symbols(limit=TOP_COINS):

    perps = set(get_perpetual_symbols())

    url = f"{FUTURES_BASE}/api/v1/contract/ticker"

    try:
        r = requests.get(url, timeout=20)

        data = r.json()["data"]

        coins = []

        for coin in data:

            symbol = coin["symbol"]

            if symbol not in perps:
                continue

            volume = float(coin.get("volume24", 0))
            last = float(coin.get("lastPrice", 0))

            coins.append({
                "symbol": symbol,
                "volume": volume,
                "price": last
            })

        coins.sort(
            key=lambda x: x["volume"],
            reverse=True
        )

        return coins[:limit]

    except Exception as e:
        print(e)
        return []


def get_klines(symbol, interval="60m", limit=200):

    interval = _INTERVAL_MAP.get(interval, "Min60")

    url = f"{FUTURES_BASE}/api/v1/contract/kline/{symbol}"

    try:

        r = requests.get(
            url,
            params={
                "interval": interval,
                "limit": limit
            },
            timeout=15
        )

        data = r.json()["data"]

        candles = []

        for i in range(len(data["time"])):

            candles.append({

                "time": data["time"][i],

                "open": float(data["open"][i]),

                "high": float(data["high"][i]),

                "low": float(data["low"][i]),

                "close": float(data["close"][i]),

                "volume": float(data["vol"][i])

            })

        return candles

    except Exception as e:
        print(symbol, e)
        return []


def scan_market(interval="60m"):

    coins = get_top_symbols()

    def fetch(coin):

        candles = get_klines(
            coin["symbol"],
            interval=interval
        )

        return {

            "symbol": coin["symbol"],

            "price": coin["price"],

            "volume": coin["volume"],

            "candles": candles

        }

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        market = list(
            executor.map(fetch, coins)
        )

    return [
        coin
        for coin in market
        if len(coin["candles"]) > 100
    ]