from pybit.unified_trading import HTTP

session = HTTP(
    testnet=False,
    api_key="YOUR_API",
    api_secret="YOUR_SECRET"
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
