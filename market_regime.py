import random

def get_market_regime():

    r = random.random()

    if r < 0.33:
        return "TREND_UP"
    elif r < 0.66:
        return "RANGE"
    return "TREND_DOWN"
