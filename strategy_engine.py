def trend_strategy(signal):
    return signal == "BUY"


def range_strategy(price_action):
    return price_action == "oversold"


def downtrend_strategy(signal):
    return False
