from config import WEBHOOK_SECRET, DEFAULT_SYMBOL, ORDER_QTY


def validate(data):

    if not isinstance(data, dict):
        return False, "invalid json"

    if data.get("secret") != WEBHOOK_SECRET:
        return False, "bad secret"

    signal = data.get("signal", "").upper()
    symbol = data.get("symbol", DEFAULT_SYMBOL)
    qty = float(data.get("qty", ORDER_QTY))

    if signal not in ["BUY", "SELL", "EXIT"]:
        return False, "bad signal"

    return True, {
        "signal": signal,
        "symbol": symbol,
        "qty": qty
    }
