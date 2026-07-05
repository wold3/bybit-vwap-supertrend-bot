from collections import deque
import statistics

# 최근 가격 저장
PRICE_HISTORY = deque(maxlen=100)


def update_price(price):
    """
    가격 히스토리 업데이트
    """
    try:
        PRICE_HISTORY.append(float(price))
    except (TypeError, ValueError):
        pass


def get_features(price):
    """
    AI 입력 Feature 생성

    Returns
    -------
    {
        price,
        sma,
        momentum,
        volatility,
        trend
    }
    """

    update_price(price)

    history = list(PRICE_HISTORY)

    if len(history) < 2:
        return {
            "price": float(price),
            "sma": float(price),
            "momentum": 0.0,
            "volatility": 0.0,
            "trend": 0.0,
        }

    # -------------------------
    # SMA
    # -------------------------
    sma = sum(history) / len(history)

    # -------------------------
    # Momentum
    # -------------------------
    momentum = history[-1] - history[0]

    # -------------------------
    # Volatility
    # -------------------------
    volatility = statistics.pstdev(history)

    # -------------------------
    # Trend
    # -------------------------
    trend = (history[-1] - sma) / sma if sma else 0.0

    return {
        "price": round(float(price), 4),
        "sma": round(sma, 4),
        "momentum": round(momentum, 4),
        "volatility": round(volatility, 4),
        "trend": round(trend, 6),
    }


def get_feature_vector(price):
    """
    DQN/PPO 입력용 벡터 반환
    """

    f = get_features(price)

    return [
        f["price"],
        f["sma"],
        f["momentum"],
        f["volatility"],
        f["trend"],
    ]


def reset():
    """
    가격 히스토리 초기화
    """

    PRICE_HISTORY.clear()
