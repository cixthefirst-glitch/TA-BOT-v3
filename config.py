import os

# ==========================
# API Keys
# ==========================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "")

MEXC_ACCESS_KEY = os.getenv("MEXC_ACCESS_KEY", "")
MEXC_SECRET_KEY = os.getenv("MEXC_SECRET_KEY", "")

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")

# ==========================
# API URLs
# ==========================

MEXC_BASE = "https://api.mexc.com"
FUTURES_BASE = "https://contract.mexc.com"

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-2.0-flash:generateContent"
)

TELEGRAM_URL = "https://api.telegram.org/bot{token}/{method}"

COINGECKO_URL = "https://api.coingecko.com/api/v3"

# ==========================
# Scanner Settings
# ==========================

TOP_COINS = 1000

MAX_WORKERS = 12

VOLATILITY_THRESHOLD = 3.0

TIMEFRAME = "60m"

# ==========================
# Risk Settings
# ==========================

MIN_RR = 2.5

ATR_SL_MULTIPLIER = 1.5

TP_LEVELS = [1, 2, 3]

# ==========================
# ML
# ==========================

ML_INFLUENCE = 0.25

MODEL_PATH = "data/model.pkl"

MODEL_COEFS = "data/model_coefs.json"

# ==========================
# Files
# ==========================

SIGNALS_FILE = "data/signals.json"

RULE_STATS_FILE = "data/rule_stats.json"

GEMINI_USAGE_FILE = "data/gemini_usage.json"

# ==========================
# Gemini
# ==========================

GEMINI_DAILY_LIMIT = 30

TOP_GEMINI_SIGNALS = 5

# ==========================
# Signal Settings
# ==========================

MIN_SCORE = 0.65

MAX_SIGNAL_AGE = 24