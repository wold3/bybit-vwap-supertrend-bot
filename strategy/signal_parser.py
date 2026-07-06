def parse_signal(data):
    """
    TradingView / API signal normalize
    """

    if isinstance(data, dict):

        return {
            "signal": data.get("signal"),
            "symbol": data.get("symbol"),
            "price": data.get("price"),
            "qty": data.get("qty", 0),
        }

    return None
