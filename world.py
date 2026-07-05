from market import Market
from agent import Agent
from evolution import Evolution
from metrics import Metrics


class World:

    def __init__(self, n_agents=6):

        self.market = Market()
        self.evo = Evolution()
        self.metrics = Metrics()

        self.agents = [Agent() for _ in range(n_agents)]

    def step(self):

        actions = [a.act(self.market.price) for a in self.agents]

        buy = sum(a == 1 for a in actions)
        sell = sum(a == 2 for a in actions)

        price = self.market.step(buy, sell)

        self.metrics.update(price)

        for i, a in enumerate(self.agents):

            if actions[i] == 1:
                a.capital -= 1

            elif actions[i] == 2:
                a.capital += 1

        self.agents = self.evo.step(self.agents)

        return price
