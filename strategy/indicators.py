import numpy as np


def sma(data, period=20):
    if len(data) < period:
        return None

    return np.mean(data[-period:])


def volatility(data, period=20):
    if len(data) < period:
        return 0

    return np.std(data[-period:])
