import random

def allow_trade():

    volatility = random.uniform(0, 1)

    if volatility < 0.3:
        return False, "low volatility"

    return True, "ok"
