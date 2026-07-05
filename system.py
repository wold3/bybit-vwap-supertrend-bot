from agent import Agent
from macro import Macro


class EconomySystem:

    def __init__(self, n_agents=3):

        self.agents = [Agent() for _ in range(n_agents)]
        self.macro = Macro()

    def step(self, price):

        liquidity, risk_on = self.macro.step()

        actions = [
            a.act(price, risk_on)
            for a in self.agents
        ]

        return actions, liquidity
