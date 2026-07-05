"""
signal_parser.py

TradingView Webhook Parser
"""

from config import DEFAULT_SYMBOL, ORDER_QTY

VALID_SIGNALS = {
    "BUY",
    "SELL",
    "SHORT",
    "EXIT"
}


class SignalError(Exception):
    pass


def normalize_signal(signal):

    if signal is None:
        raise SignalError("signal is missing")

    signal = str(signal).strip().upper()

    if signal not in VALID_SIGNALS:
        raise SignalError(f"invalid signal : {signal}")

    return signal


def normalize_symbol(symbol):

    if symbol is None:
        return DEFAULT_SYMBOL

    symbol = str(symbol).strip().upper()

    if symbol == "":
        return DEFAULT_SYMBOL

    return symbol


def normalize_qty(qty):

    if qty is None:
        return ORDER_QTY

    try:

        qty = float(qty)

    except Exception:

        raise SignalError("qty must be numeric")

    if qty <= 0:
        raise SignalError("qty must be greater than zero")

    return qty


def parse_webhook(data):

    if data is None:
        raise SignalError("empty json")

    if not isinstance(data, dict):
        raise SignalError("json object expected")

    signal = normalize_signal(
        data.get("signal")
    )

    symbol = normalize_symbol(
        data.get("symbol")
    )

    qty = normalize_qty(
        data.get("qty")
    )

    return {
        "signal": signal,
        "symbol": symbol,
        "qty": qty
    }


def validate(data):

    try:

        result = parse_webhook(data)

        return True, result

    except Exception as e:

        return False, str(e)


if __name__ == "__main__":

    sample = {
        "signal": "BUY",
        "symbol": "BTCUSDT",
        "qty": 0.001
    }

    ok, result = validate(sample)

    print(ok)

    print(result)
