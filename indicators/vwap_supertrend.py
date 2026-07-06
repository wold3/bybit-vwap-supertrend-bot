import numpy as np


# =================================================
# VWAP 계산
# =================================================
def calculate_vwap(prices, volumes):

    prices = np.array(prices)
    volumes = np.array(volumes)

    return np.sum(prices * volumes) / np.sum(volumes)


# =================================================
# SUPER TREND (단순 버전)
# =================================================
def supertrend(prices, period=10):

    prices = np.array(prices)

    atr = np.mean(np.abs(np.diff(prices)))

    hl2 = (prices[-1] + prices[-2]) / 2

    upper = hl2 + atr
    lower = hl2 - atr

    if prices[-1] > upper:
        return "UP"
    elif prices[-1] < lower:
        return "DOWN"
    else:
        return "FLAT"
