import random


class Agent:

    def __init__(self, name="agent"):
        self.name = name
        self.position = 0
        self.capital = 1000

    def act(self, price):

        # 간단한 momentum + noise 전략
        signal = price * random.uniform(-0.01, 0.01)

        if random.random() < 0.1:
            return random.randint(0, 2)

        if signal > 0:
            return 1  # BUY
        elif signal < 0:
            return 2  # SELL

        return 0  # HOLD

    def update(self, reward):
        self.capital += reward
