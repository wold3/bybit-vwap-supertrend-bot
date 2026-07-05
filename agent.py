import random


class Agent:

    def __init__(self):
        self.position = 0
        self.capital = 1000

    def act(self, price, risk_on):

        if not risk_on:
            return 2

        signal = random.uniform(-1, 1)

        if signal > 0.3:
            return 1
        elif signal < -0.3:
            return 2

        return 0

    def update(self, pnl):
        self.capital += pnl
