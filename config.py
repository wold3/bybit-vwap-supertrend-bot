import os
from dotenv import load_dotenv

load_dotenv()

BYBIT_API_KEY = os.getenv("BYBIT_API_KEY", "")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET", "")

TESTNET = os.getenv("TESTNET", "True").lower() == "true"

CATEGORY = "linear"
ACCOUNT_TYPE = "UNIFIED"

DEFAULT_SYMBOL = os.getenv("DEFAULT_SYMBOL", "BTCUSDT")
ORDER_QTY = float(os.getenv("ORDER_QTY", "0.001"))

POSITION_IDX = int(os.getenv("POSITION_IDX", "0"))
LEVERAGE = int(os.getenv("LEVERAGE", "5"))

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

MAX_DAILY_LOSS = float(os.getenv("MAX_DAILY_LOSS", "50"))

TRADE_LOG = "logs/trade.log"
WEBHOOK_LOG = "logs/webhook.log"
