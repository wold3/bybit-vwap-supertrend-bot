import random


class MarketSimulator:

    def __init__(self, price=100.0):
        self.price = price
        self.volatility = 0.01

    def step(self, buy_pressure, sell_pressure):

        imbalance = buy_pressure - sell_pressure

        noise = random.gauss(0, self.volatility)

        self.price *= (1 + 0.001 * imbalance + noise)

        return self.price
