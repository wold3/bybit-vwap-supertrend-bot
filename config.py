import os
from dotenv import load_dotenv

load_dotenv()

BYBIT_API_KEY = os.getenv("BYBIT_API_KEY", "")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET", "")

TESTNET = os.getenv("TESTNET", "True").lower() == "true"

CATEGORY = "linear"
POSITION_IDX = int(os.getenv("POSITION_IDX", "0"))

SYMBOLS = os.getenv("SYMBOLS", "BTCUSDT,ETHUSDT").split(",")

ORDER_QTY = float(os.getenv("ORDER_QTY", "0.001"))

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

TAKE_PROFIT_PCT = float(os.getenv("TAKE_PROFIT_PCT", "1.5"))
STOP_LOSS_PCT = float(os.getenv("STOP_LOSS_PCT", "1.0"))
