from market import Market


class Environment:

    def __init__(self, n_agents=3):

        self.market = Market()
        self.positions = [0] * n_agents

    def step(self, actions, liquidity):

        buy = sum(a == 1 for a in actions)
        sell = sum(a == 2 for a in actions)

        price = self.market.step(buy, sell, liquidity)

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
