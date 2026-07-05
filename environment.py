from market import Market


class Environment:

    def __init__(self, n_agents=3):

        self.market = Market()
        self.n_agents = n_agents
        self.positions = [0] * n_agents

    def step(self, actions):

        buy = sum(1 for a in actions if a == 1)
        sell = sum(1 for a in actions if a == 2)

        price = self.market.step(buy, sell)

        rewards = []

        for i, a in enumerate(actions):

            reward = 0

            if a == 1:
                self.positions[i] = price

            elif a == 2 and self.positions[i] != 0:
                reward = price - self.positions[i]
                self.positions[i] = 0

            rewards.append(reward)

        return price, rewards
