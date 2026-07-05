from market_regime import get_market_regime
from risk_engine import should_stop


def trend_strategy(signal, regime):
    """
    추세 전략
    """

    signal = signal.upper()

    if regime == "TREND_UP":
        return signal == "BUY"

    if regime == "TREND_DOWN":
        return signal in ("SELL", "SHORT")

    return False


def range_strategy(signal, regime):
    """
    횡보 전략
    """

    signal = signal.upper()

    if regime != "RANGE":
        return False

    return signal in (
        "BUY",
        "SELL",
    )


def safe_strategy(regime):
    """
    안전 전략
    """

    return regime == "SAFE"


def select_strategy(signal, price):
    """
    현재 시장에 맞는 전략 선택

    Returns
    -------
    (allow_trade, strategy_name, regime)
    """

    if should_stop():
        return False, "risk_stop", "SAFE"

    regime = get_market_regime(price)

    if trend_strategy(signal, regime):
        return True, "trend", regime

    if range_strategy(signal, regime):
        return True, "range", regime

    if safe_strategy(regime):
        return False, "safe", regime

    return False, "none", regime
