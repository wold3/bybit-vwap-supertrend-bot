import statistics
from collections import deque

PRICE_HISTORY = deque(maxlen=200)


def update_price(price):
    try:
        PRICE_HISTORY.append(float(price))
    except:
        pass


def get_feature_vector(price, orderbook=None):

    update_price(price)

    h = list(PRICE_HISTORY)

    if len(h) < 10:
        return [float(price), 0.0, 0.0, 0.0, 0.0]

    sma = sum(h) / len(h)
    trend = (h[-1] - sma) / sma if sma else 0.0
    vol = statistics.pstdev(h)

    spread = 0.0
    imbalance = 0.0

    if orderbook:

        bids = orderbook.get("bids", [])
        asks = orderbook.get("asks", [])

        if bids and asks:

            bid_vol = sum(float(b[1]) for b in bids[:5])
            ask_vol = sum(float(a[1]) for a in asks[:5])

            spread = float(asks[0][0]) - float(bids[0][0])
            imbalance = (bid_vol - ask_vol) / (bid_vol + ask_vol + 1e-6)

    return [
        float(price),
        float(trend),
        float(vol),
        float(spread),
        float(imbalance),
    ]
