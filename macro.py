import random


class Macro:

    def __init__(self):
        self.liquidity = 10000
        self.risk_on = True

    def step(self):

        shock = random.uniform(-0.01, 0.01)
        self.liquidity *= (1 + shock)

        self.risk_on = self.liquidity > 9000

        return self.liquidity, self.risk_on
