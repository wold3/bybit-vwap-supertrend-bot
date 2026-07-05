import random

FEE_RATE = 0.0006
SLIPPAGE_BASE = 0.0005


def apply_slippage(price, volatility=1.0):

    slippage = SLIPPAGE_BASE * (1 + volatility)

    direction = 1 if random.random() > 0.5 else -1

    return price * (1 + slippage * direction)


def apply_fee(value):
    return value * (1 - FEE_RATE)


def simulate_execution(price, qty, volatility=1.0):

    exec_price = apply_slippage(price, volatility)
    cost = exec_price * qty
    cost = apply_fee(cost)

    return exec_price, cost
