from rl_agent import RLAgent

agent = RLAgent()

def decide(price):

    state = [price, 0, 0]

    return agent.act(state)
