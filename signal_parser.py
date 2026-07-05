from config import DEFAULT_SYMBOL, ORDER_QTY, WEBHOOK_SECRET


class SignalError(Exception):
    pass


def validate_secret(data):

    if WEBHOOK_SECRET == "":
        return True

    if data.get("secret") != WEBHOOK_SECRET:
        raise SignalError("invalid secret")

    return True


def parse_webhook(data):

    if not isinstance(data, dict):
        raise SignalError("invalid json")

    validate_secret(data)

    signal = str(data.get("signal", "")).upper()
    symbol = data.get("symbol", DEFAULT_SYMBOL)
    qty = data.get("qty", ORDER_QTY)

    if signal not in ["BUY", "SELL", "SHORT", "EXIT"]:
        raise SignalError("invalid signal")

    try:
        qty = float(qty)
    except:
        raise SignalError("invalid qty")

    return {
        "signal": signal,
        "symbol": symbol,
        "qty": qty
    }


def validate(data):

    try:
        return True, parse_webhook(data)
    except Exception as e:
        return False, str(e)
