import random


class Market:

    def __init__(self, price=100.0):
        self.price = price

    def step(self, buy_flow, sell_flow, liquidity):

        imbalance = buy_flow - sell_flow
        macro = liquidity / 10000

        noise = random.gauss(0, 0.01)

        self.price *= (1 + 0.001 * imbalance * macro + noise)

        return self.price
