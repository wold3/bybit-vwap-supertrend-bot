from collections import deque
import statistics

# 최근 가격 저장
PRICE_HISTORY = deque(maxlen=100)


def update_price(price):
    """
    최근 가격 저장
    """
    try:
        PRICE_HISTORY.append(float(price))
    except (TypeError, ValueError):
        pass


def get_market_regime(price):
    """
    현재 시장 상태 판단

    Returns
    -------
    TREND_UP
    TREND_DOWN
    RANGE
    HIGH_VOLATILITY
    SAFE
    """

    update_price(price)

    history = list(PRICE_HISTORY)

    if len(history) < 20:
        return "SAFE"

    sma = sum(history) / len(history)

    volatility = statistics.pstdev(history)

    trend = (history[-1] - sma) / sma

    # 변동성이 매우 큰 경우
    if volatility > sma * 0.02:
        return "HIGH_VOLATILITY"

    # 상승 추세
    if trend > 0.01:
        return "TREND_UP"

    # 하락 추세
    if trend < -0.01:
        return "TREND_DOWN"

    # 횡보
    return "RANGE"


def get_market_score(price):
    """
    시장 점수 (-1 ~ 1)
    """

    update_price(price)

    history = list(PRICE_HISTORY)

    if len(history) < 20:
        return 0.0

    sma = sum(history) / len(history)

    return round((history[-1] - sma) / sma, 4)


def reset():
    """
    히스토리 초기화
    """

    PRICE_HISTORY.clear()
