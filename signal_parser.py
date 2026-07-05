from config import (
    WEBHOOK_SECRET,
    DEFAULT_SYMBOL,
    ORDER_QTY,
)

VALID_SIGNALS = {
    "BUY",
    "SELL",
    "SHORT",
    "EXIT",
    "HOLD",
}


def validate(data):
    """
    TradingView Webhook 데이터 검증
    """

    if not isinstance(data, dict):
        return False, "Request body must be JSON."

    # -------------------------
    # Secret
    # -------------------------
    secret = data.get("secret")

    if secret != WEBHOOK_SECRET:
        return False, "Invalid webhook secret."

    # -------------------------
    # Signal
    # -------------------------
    signal = str(
        data.get("signal", "BUY")
    ).upper()

    if signal not in VALID_SIGNALS:
        return False, f"Invalid signal: {signal}"

    # -------------------------
    # Symbol
    # -------------------------
    symbol = str(
        data.get("symbol", DEFAULT_SYMBOL)
    ).upper()

    if len(symbol) < 6:
        return False, "Invalid symbol."

    # -------------------------
    # Quantity
    # -------------------------
    try:
        qty = float(
            data.get("qty", ORDER_QTY)
        )
    except (ValueError, TypeError):
        return False, "Quantity must be numeric."

    if qty <= 0:
        return False, "Quantity must be greater than zero."

    # -------------------------
    # Price (Optional)
    # -------------------------
    try:
        price = float(
            data.get("price", 0)
        )
    except (ValueError, TypeError):
        return False, "Price must be numeric."

    # -------------------------
    # Return
    # -------------------------
    return True, {
        "signal": signal,
        "symbol": symbol,
        "qty": qty,
        "price": price,
    }
