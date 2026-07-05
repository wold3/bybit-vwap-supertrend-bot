from pybit.unified_trading import HTTP
from config import TESTNET

API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"

session = HTTP(
    testnet=TESTNET,
    api_key=API_KEY,
    api_secret=API_SECRET
)


def execute(signal, symbol, qty):

    if signal == "BUY":
        return session.place_order(
            category="linear",
            symbol=symbol,
            side="Buy",
            orderType="Market",
            qty=str(qty)
        )

    elif signal in ["SELL", "SHORT", "EXIT"]:
        return session.place_order(
            category="linear",
            symbol=symbol,
            side="Sell",
            orderType="Market",
            qty=str(qty)
        )

    return {"error": "invalid signal"}
