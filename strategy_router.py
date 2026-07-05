from market_regime import get_market_regime


def should_trade(signal):

    regime = get_market_regime()

    if regime == "TREND_UP":
        return True, regime

    if regime == "RANGE":
        return False, regime

    if regime == "TREND_DOWN":
        return False, regime

    return False, "UNKNOWN"
