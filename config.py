SYMBOLS = ["BTCUSDT"]

MODE = "PAPER"  # PAPER | LIVE

BYBIT_TESTNET = True

MAX_DAILY_LOSS = -50import os
from dotenv import load_dotenv

load_dotenv()


# 거래 심볼
SYMBOLS = [
    "BTCUSDT"
]


# 실행 모드
# PAPER : 모의매매
# LIVE  : 실거래
MODE = "PAPER"


# Bybit 환경
BYBIT_TESTNET = True


# 리스크 관리
MAX_DAILY_LOSS = -50
MAX_TRADES = 100


# Telegram 알림 설정
TELEGRAM_TOKEN = os.getenv(
    "TELEGRAM_TOKEN",
    ""
)

TELEGRAM_CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID",
    ""
)


# API 설정 (추후 사용)
BYBIT_API_KEY = os.getenv(
    "BYBIT_API_KEY",
    ""
)

BYBIT_API_SECRET = os.getenv(
    "BYBIT_API_SECRET",
    ""
)
MAX_TRADES = 100
