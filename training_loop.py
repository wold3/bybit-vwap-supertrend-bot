from config import (
    BATCH_SIZE,
    MODEL_PATH,
)

from env import TradingEnv
from dqn_agent import Agent


def train(
    prices,
    episodes=20,
):
    """
    DQN 학습 루프
    """

    env = TradingEnv()

    agent = Agent()

    for episode in range(episodes):

        state = env.reset()

        total_reward = 0.0

        last_loss = None

        for price in prices:

            action = agent.act(state)

            next_state, reward, done = env.step(
                action,
                price,
            )

            agent.remember(
                state,
                action,
                reward,
                next_state,
                done,
            )

            loss = agent.train(BATCH_SIZE)

            if loss is not None:
                last_loss = loss

            total_reward += reward

            state = next_state

            if done:
                break

        agent.update_target()

        print(
            f"Episode {episode + 1}/{episodes} | "
            f"Reward={total_reward:.2f} | "
            f"Loss={last_loss if last_loss is not None else '-'} | "
            f"Epsilon={agent.epsilon:.4f}"
        )

    agent.save(MODEL_PATH)

    print(f"Model saved to {MODEL_PATH}")

    return agent
