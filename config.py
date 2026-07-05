import os
from dotenv import load_dotenv

# =====================================================
# Environment
# =====================================================

load_dotenv()

# =====================================================
# Bybit API
# =====================================================

BYBIT_API_KEY = os.getenv("BYBIT_API_KEY", "")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET", "")
TESTNET = os.getenv("TESTNET", "False").lower() == "true"

# =====================================================
# Webhook
# =====================================================

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "1234")

# =====================================================
# Trading
# =====================================================

DEFAULT_SYMBOL = os.getenv("DEFAULT_SYMBOL", "BTCUSDT")

ORDER_QTY = float(os.getenv("ORDER_QTY", "0.001"))

LEVERAGE = int(os.getenv("LEVERAGE", "10"))

MAX_TRADES_PER_MIN = int(
    os.getenv("MAX_TRADES_PER_MIN", "3")
)

# =====================================================
# Position Sizing
# =====================================================

MIN_ORDER_QTY = float(
    os.getenv("MIN_ORDER_QTY", "0.001")
)

MAX_ORDER_QTY = float(
    os.getenv("MAX_ORDER_QTY", "10")
)

RISK_PER_TRADE = float(
    os.getenv("RISK_PER_TRADE", "0.01")
)

# =====================================================
# Risk
# =====================================================

MAX_DAILY_LOSS = float(
    os.getenv("MAX_DAILY_LOSS", "50")
)

MAX_LOSS_STREAK = int(
    os.getenv("MAX_LOSS_STREAK", "5")
)

STOP_LOSS_PERCENT = float(
    os.getenv("STOP_LOSS_PERCENT", "1.0")
)

TAKE_PROFIT_PERCENT = float(
    os.getenv("TAKE_PROFIT_PERCENT", "2.0")
)

TRAILING_STOP_PERCENT = float(
    os.getenv("TRAILING_STOP_PERCENT", "0.5")
)

# =====================================================
# Telegram
# =====================================================

TELEGRAM_TOKEN = os.getenv(
    "TELEGRAM_TOKEN",
    ""
)

TELEGRAM_CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID",
    ""
)

# =====================================================
# Logging
# =====================================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)

LOG_FILE = os.getenv(
    "LOG_FILE",
    "logs/bot.log"
)

# =====================================================
# Database
# =====================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///trading.db"
)

# =====================================================
# AI / RL
# =====================================================

MODEL_PATH = os.getenv(
    "MODEL_PATH",
    "models/best_model.zip"
)

REPLAY_BUFFER_SIZE = int(
    os.getenv("REPLAY_BUFFER_SIZE", "10000")
)

BATCH_SIZE = int(
    os.getenv("BATCH_SIZE", "64")
)

LEARNING_RATE = float(
    os.getenv("LEARNING_RATE", "0.0003")
)

GAMMA = float(
    os.getenv("GAMMA", "0.99")
)

EPSILON = float(
    os.getenv("EPSILON", "0.10")
)

EPSILON_MIN = float(
    os.getenv("EPSILON_MIN", "0.01")
)

EPSILON_DECAY = float(
    os.getenv("EPSILON_DECAY", "0.995")
)

TARGET_UPDATE = int(
    os.getenv("TARGET_UPDATE", "100")
)

# =====================================================
# Flask
# =====================================================

HOST = os.getenv("HOST", "0.0.0.0")

PORT = int(
    os.getenv("PORT", "5000")
)

DEBUG = os.getenv(
    "DEBUG",
    "False"
).lower() == "true"
