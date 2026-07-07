import os
from dotenv import load_dotenv

load_dotenv()


# =========================
# Trading Symbol
# =========================

SYMBOLS = [
    "BTCUSDT"
]


# =========================
# Mode
# =========================

# PAPER : 모의매매
# LIVE  : 실거래

MODE = "PAPER"


# =========================
# Bybit Settings
# =========================

BYBIT_TESTNET = True


BYBIT_API_KEY = os.getenv(
    "BYBIT_API_KEY",
    ""
)

BYBIT_API_SECRET = os.getenv(
    "BYBIT_API_SECRET",
    ""
)


# =========================
# Risk Management
# =========================

MAX_DAILY_LOSS = -50

MAX_TRADES = 100


# =========================
# Telegram Notification
# =========================

TELEGRAM_TOKEN = os.getenv(
    "TELEGRAM_TOKEN",
    ""
)

TELEGRAM_CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID",
    ""
)
