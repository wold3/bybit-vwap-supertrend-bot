from env import TradingEnv
from dqn_agent import Agent

def train(prices):

    env = TradingEnv()
    agent = Agent()

    for ep in range(10):

        state = env.reset()

        for price in prices:

            action = agent.act(state)

            next_state, reward = env.step(action, price)

            agent.buffer.push(state, action, reward, next_state)

            agent.train()

            state = next_state

        agent.update_target()

    return agent
