import statistics
from collections import deque

PRICE_HISTORY = deque(maxlen=200)


def update_price(price):
    try:
        PRICE_HISTORY.append(float(price))
    except:
        pass


# ==========================
# BASIC FEATURES
# ==========================

def get_basic_features(price):

    update_price(price)

    h = list(PRICE_HISTORY)

    if len(h) < 10:
        return {
            "price": float(price),
            "trend": 0.0,
            "volatility": 0.0,
        }

    sma = sum(h) / len(h)
    volatility = statistics.pstdev(h)
    trend = (h[-1] - sma) / sma if sma else 0.0

    return {
        "price": float(price),
        "trend": trend,
        "volatility": volatility,
    }


# ==========================
# VOLATILITY REGIME
# ==========================

def get_volatility_regime(price):

    h = list(PRICE_HISTORY)

    if len(h) < 20:
        return 0  # LOW

    vol = statistics.pstdev(h[-20:])

    if vol < 1:
        return 0  # LOW
    elif vol < 3:
        return 1  # MID
    else:
        return 2  # HIGH


# ==========================
# ORDERBOOK FEATURES
# ==========================

def get_orderbook_features(orderbook):

    if not orderbook:
        return 0.0, 0.0

    bids = orderbook.get("bids", [])
    asks = orderbook.get("asks", [])

    if not bids or not asks:
        return 0.0, 0.0

    bid_vol = sum(float(b[1]) for b in bids[:5])
    ask_vol = sum(float(a[1]) for a in asks[:5])

    spread = float(asks[0][0]) - float(bids[0][0])
    imbalance = (bid_vol - ask_vol) / (bid_vol + ask_vol + 1e-6)

    return spread, imbalance


# ==========================
# FINAL FEATURE VECTOR
# ==========================

def get_feature_vector(price, orderbook=None):

    basic = get_basic_features(price)
    regime = get_volatility_regime(price)

    spread, imbalance = get_orderbook_features(orderbook)

    return [
        basic["price"],
        basic["trend"],
        basic["volatility"],
        spread,
        imbalance,
        float(regime == 2),  # HIGH
        float(regime == 1),  # MID
    ]
