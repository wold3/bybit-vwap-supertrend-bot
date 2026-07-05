from environment import MarketEnv
from world_agent import WorldAgent


def train():

    env = MarketEnv()
    agents = [WorldAgent() for _ in range(3)]

    price = 100

    for step in range(500):

        actions = [a.act([price] * 5) for a in agents]

        price, rewards = env.step(actions)

        for i, agent in enumerate(agents):
            pass  # placeholder learning hook

    return agents
