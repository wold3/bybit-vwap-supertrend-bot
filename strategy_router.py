from market_regime import get_market_regime
from strategy_engine import trend_strategy, range_strategy, downtrend_strategy


def route(signal, price_action):

    regime = get_market_regime()

    if regime == "TREND_UP":
        return trend_strategy(signal), regime

    if regime == "RANGE":
        return range_strategy(price_action), regime

    if regime == "TREND_DOWN":
        return downtrend_strategy(signal), regime

    return False, regime
