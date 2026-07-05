import random
from dqn_agent import Agent

agent = Agent()

def decide(price):

    state = [price, 0, 0]

    return agent.act(state)
