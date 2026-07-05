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

TAKE_PROFIT_PCT = float(os.getenv("TAKE_PROFIT_PCT", "1.5"))
STOP_LOSS_PCT = float(os.getenv("STOP_LOSS_PCT", "1.0"))

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

TRADE_LOG = "logs/trade.log"
WEBHOOK_LOG = "logs/webhook.log"
