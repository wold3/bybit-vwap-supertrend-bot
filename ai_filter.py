import random

def allow_trade():

    if random.random() < 0.3:
        return False, "low volatility"

    return True, "ok"
