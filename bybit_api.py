from pybit.unified_trading import HTTP
from config import TESTNET

session = HTTP(
    testnet=TESTNET,
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET"
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

    if signal in ["SELL", "EXIT"]:
        return session.place_order(
            category="linear",
            symbol=symbol,
            side="Sell",
            orderType="Market",
            qty=str(qty)
        )

    return {"error": "invalid"}
