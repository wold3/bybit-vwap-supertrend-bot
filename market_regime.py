import random

def get_market_regime():

    r = random.uniform(0, 1)

    if r < 0.33:
        return "TREND_UP"

    elif r < 0.66:
        return "RANGE"

    else:
        return "TREND_DOWN"
