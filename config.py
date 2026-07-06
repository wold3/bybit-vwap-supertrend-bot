from pathlib import Path
import os

from dotenv import load_dotenv

# =====================================================
# Base Path
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

# =====================================================
# Helper Functions
# =====================================================


def env_str(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def env_int(name: str, default: int) -> int:
    return int(os.getenv(name, str(default)))


def env_float(name: str, default: float) -> float:
    return float(os.getenv(name, str(default)))


def env_bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).lower() == "true"


# =====================================================
# Directories
# =====================================================

LOG_DIR = BASE_DIR / "logs"
MODEL_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"

LOG_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# =====================================================
# Bybit API
# =====================================================

BYBIT_API_KEY = env_str("BYBIT_API_KEY")
BYBIT_API_SECRET = env_str("BYBIT_API_SECRET")
TESTNET = env_bool("TESTNET", True)

# =====================================================
# Webhook
# =====================================================

WEBHOOK_SECRET = env_str("WEBHOOK_SECRET", "1234")

# =====================================================
# Trading
# =====================================================

DEFAULT_SYMBOL = env_str("DEFAULT_SYMBOL", "BTCUSDT")

ORDER_QTY = env_float("ORDER_QTY", 0.001)

LEVERAGE = env_int("LEVERAGE", 10)

MAX_TRADES_PER_MIN = env_int(
    "MAX_TRADES_PER_MIN",
    3,
)

# =====================================================
# Position Sizing
# =====================================================

MIN_ORDER_QTY = env_float(
    "MIN_ORDER_QTY",
    0.001,
)

MAX_ORDER_QTY = env_float(
    "MAX_ORDER_QTY",
    10.0,
)

RISK_PER_TRADE = env_float(
    "RISK_PER_TRADE",
    0.01,
)

# =====================================================
# Risk Management
# =====================================================

MAX_DAILY_LOSS = env_float(
    "MAX_DAILY_LOSS",
    50.0,
)

MAX_LOSS_STREAK = env_int(
    "MAX_LOSS_STREAK",
    5,
)

STOP_LOSS_PERCENT = env_float(
    "STOP_LOSS_PERCENT",
    1.0,
)

TAKE_PROFIT_PERCENT = env_float(
    "TAKE_PROFIT_PERCENT",
    2.0,
)

TRAILING_STOP_PERCENT = env_float(
    "TRAILING_STOP_PERCENT",
    0.5,
)

# =====================================================
# Telegram
# =====================================================

TELEGRAM_TOKEN = env_str(
    "TELEGRAM_TOKEN",
)

TELEGRAM_CHAT_ID = env_str(
    "TELEGRAM_CHAT_ID",
)

# =====================================================
# Logging
# =====================================================

LOG_LEVEL = env_str(
    "LOG_LEVEL",
    "INFO",
)

LOG_FILE = env_str(
    "LOG_FILE",
    str(LOG_DIR / "bot.log"),
)

# =====================================================
# Database
# =====================================================

DATABASE_URL = env_str(
    "DATABASE_URL",
    f"sqlite:///{DATA_DIR / 'trading.db'}",
)

# =====================================================
# AI / RL
# =====================================================

MODEL_PATH = env_str(
    "MODEL_PATH",
    str(MODEL_DIR / "best_model.pth"),
)

REPLAY_BUFFER_SIZE = env_int(
    "REPLAY_BUFFER_SIZE",
    10000,
)

BATCH_SIZE = env_int(
    "BATCH_SIZE",
    64,
)

LEARNING_RATE = env_float(
    "LEARNING_RATE",
    0.0003,
)

GAMMA = env_float(
    "GAMMA",
    0.99,
)

EPSILON = env_float(
    "EPSILON",
    0.10,
)

EPSILON_MIN = env_float(
    "EPSILON_MIN",
    0.01,
)

EPSILON_DECAY = env_float(
    "EPSILON_DECAY",
    0.995,
)

TARGET_UPDATE = env_int(
    "TARGET_UPDATE",
    100,
)

# =====================================================
# Backtest
# =====================================================

INITIAL_BALANCE = env_float(
    "INITIAL_BALANCE",
    1000.0,
)

# =====================================================
# Watchdog
# =====================================================

CHECK_INTERVAL = env_int(
    "CHECK_INTERVAL",
    10,
)

MAX_RESTART = env_int(
    "MAX_RESTART",
    20,
)

# =====================================================
# Flask
# =====================================================

HOST = env_str(
    "HOST",
    "0.0.0.0",
)

PORT = env_int(
    "PORT",
    5000,
)

DEBUG = env_bool(
    "DEBUG",
    False,
)

# =====================================================
# Validation
# =====================================================


def validate() -> None:
    """
    Validate configuration values.
    Call this once during application startup.
    """

    if not TESTNET:
        if not BYBIT_API_KEY:
            raise ValueError("BYBIT_API_KEY is missing.")

        if not BYBIT_API_SECRET:
            raise ValueError("BYBIT_API_SECRET is missing.")

    if ORDER_QTY <= 0:
        raise ValueError("ORDER_QTY must be greater than zero.")

    if MIN_ORDER_QTY <= 0:
        raise ValueError("MIN_ORDER_QTY must be greater than zero.")

    if MAX_ORDER_QTY <= 0:
        raise ValueError("MAX_ORDER_QTY must be greater than zero.")

    if MIN_ORDER_QTY > MAX_ORDER_QTY:
        raise ValueError(
            "MIN_ORDER_QTY cannot exceed MAX_ORDER_QTY."
        )

    if LEVERAGE < 1:
        raise ValueError(
            "LEVERAGE must be at least 1."
        )

    if not (0.0 <= RISK_PER_TRADE <= 1.0):
        raise ValueError(
            "RISK_PER_TRADE must be between 0 and 1."
        )

    if STOP_LOSS_PERCENT <= 0:
        raise ValueError(
            "STOP_LOSS_PERCENT must be greater than zero."
        )

    if TAKE_PROFIT_PERCENT <= 0:
        raise ValueError(
            "TAKE_PROFIT_PERCENT must be greater than zero."
        )

    if TRAILING_STOP_PERCENT < 0:
        raise ValueError(
            "TRAILING_STOP_PERCENT cannot be negative."
        )
