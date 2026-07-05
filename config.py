"""
config.py
Bybit VWAP SuperTrend Bot
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ======================================
# API
# ======================================

BYBIT_API_KEY = os.getenv("BYBIT_API_KEY", "")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET", "")

TESTNET = os.getenv("TESTNET", "True").lower() == "true"

# ======================================
# Trading
# ======================================

CATEGORY = "linear"

ACCOUNT_TYPE = "UNIFIED"

DEFAULT_SYMBOL = os.getenv(
    "DEFAULT_SYMBOL",
    "BTCUSDT"
)

ORDER_QTY = float(
    os.getenv(
        "ORDER_QTY",
        "0.001"
    )
)

# ======================================
# Position Mode
# 0 = OneWay
# 1 = Hedge Buy
# 2 = Hedge Sell
# ======================================

POSITION_IDX = int(
    os.getenv(
        "POSITION_IDX",
        "0"
    )
)

# ======================================
# Leverage
# ======================================

LEVERAGE = int(
    os.getenv(
        "LEVERAGE",
        "5"
    )
)

# ======================================
# Order
# ======================================

ORDER_TYPE = "Market"

TIME_IN_FORCE = "IOC"

RECV_WINDOW = 5000

# ======================================
# Flask
# ======================================

HOST = "0.0.0.0"

PORT = 5000

DEBUG = False

# ======================================
# Security
# ======================================

WEBHOOK_SECRET = os.getenv(
    "WEBHOOK_SECRET",
    ""
)

# ======================================
# Log
# ======================================

LOG_PATH = "logs"

TRADE_LOG = "logs/trade.log"

WEBHOOK_LOG = "logs/webhook.log"
