from agent import Agent


class AgentSystem:

    def __init__(self, n=3):

        self.agents = [Agent(f"A{i}") for i in range(n)]

    def act_all(self, price):

        return [a.act(price) for a in self.agents]

    def update_all(self, rewards):

        for i, a in enumerate(self.agents):
            a.update(rewards[i])
