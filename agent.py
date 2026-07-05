import random


class Agent:

    def __init__(self):
        self.capital = 1000
        self.strategy = random.uniform(-1, 1)

    def act(self, price):

        signal = price * self.strategy * random.uniform(-0.01, 0.01)

        if signal > 0.2:
            return 1
        elif signal < -0.2:
            return 2

        return 0

    def fitness(self):
        return self.capital

    def mutate(self):

        child = Agent()
        child.strategy = self.strategy + random.uniform(-0.2, 0.2)
        return child
