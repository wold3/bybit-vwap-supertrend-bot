import random

class RLAgent:

    def __init__(self):
        self.q = {}

    def act(self, state):
        return random.choice([0, 1, 2])

    def learn(self, state, action, reward):

        key = str(state)

        if key not in self.q:
            self.q[key] = [0, 0, 0]

        self.q[key][action] += reward * 0.01
