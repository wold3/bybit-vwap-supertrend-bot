import numpy as np


def route(signal, price):
    """
    시장 상태 판단 (regime detection)
    """

    # 매우 단순한 실전용 placeholder 구조
    # (추후 indicators.py에서 확장)

    if signal is None:
        return False, "NONE"

    # fake volatility proxy
    volatility = np.random.random()

    if volatility > 0.7:
        return True, "TREND_UP"

    elif volatility > 0.3:
        return True, "RANGE"

    else:
        return False, "LOW_VOL"
