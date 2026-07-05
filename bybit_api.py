from pybit.unified_trading import HTTP

from config import BYBIT_API_KEY, BYBIT_API_SECRET, TESTNET

session = HTTP(
    testnet=TESTNET,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET,
)


def execute(signal, symbol, qty):

    signal = signal.upper()

    if signal == "BUY":
        side = "Buy"
    elif signal in ("SELL", "SHORT", "EXIT"):
        side = "Sell"
    else:
        raise ValueError(f"Unknown signal: {signal}")

    try:
        response = session.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=str(qty),
            timeInForce="IOC",
        )

        return {"success": True, "response": response}

    except Exception as e:
        return {"success": False, "error": str(e)}


def get_unrealized_pnl(symbol):

    try:
        result = session.get_positions(
            category="linear",
            symbol=symbol,
        )

        positions = result.get("result", {}).get("list", [])

        if not positions:
            return 0.0

        return float(positions[0].get("unrealisedPnl", 0))

    except Exception:
        return 0.0
