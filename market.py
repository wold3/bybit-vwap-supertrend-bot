import random


class Market:

    def __init__(self, price=100.0):
        self.price = price

    def step(self, buy, sell):

        imbalance = buy - sell
        noise = random.gauss(0, 0.01)

        self.price *= (1 + 0.001 * imbalance + noise)

        return self.price
