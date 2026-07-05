class TradingEnv:

    def __init__(self):
        self.balance = 1000
        self.position = 0
        self.entry = 0

    def reset(self):
        self.balance = 1000
        self.position = 0
        self.entry = 0
        return self.state()

    def state(self):
        return [self.balance, self.position, self.entry]

    def step(self, action, price):

        reward = 0

        if action == 1 and self.position == 0:
            self.position = 1
            self.entry = price

        elif action == 2 and self.position == 1:
            reward = price - self.entry
            self.balance += reward
            self.position = 0

        elif action == 0:
            reward = -0.01

        return self.state(), reward
