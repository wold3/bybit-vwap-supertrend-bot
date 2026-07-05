from config import WEBHOOK_SECRET, DEFAULT_SYMBOL, ORDER_QTY

def validate(data):

    if not isinstance(data, dict):
        return False, "invalid"

    if data.get("secret") != WEBHOOK_SECRET:
        return False, "bad secret"

    return True, {
        "symbol": data.get("symbol", DEFAULT_SYMBOL),
        "qty": float(data.get("qty", ORDER_QTY))
    }
