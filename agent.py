import random


class Agent:

    def act(self, price):

        if random.random() < 0.1:
            return random.randint(0, 2)

        if price % 2 > 1:
            return 1
        else:
            return 2

    def learn(self, reward):
        pass
