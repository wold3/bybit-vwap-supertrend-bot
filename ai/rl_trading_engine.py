import numpy as np

from collections import deque
from ai.trading_brain import brain


class RLTradingEngine:

    def __init__(self):

        self.memory = deque(maxlen=1000)

        self.gamma = 0.95  # discount factor
        self.learning_rate = 0.01

        self.policy_score = {
            "trend": 0.5,
            "range": 0.5,
            "safe": 0.5
        }

    # =====================================================
    # 상태 정의
    # =====================================================

    def get_state(self, price):

        return np.array([
            price % 100,
            np.random.rand(),  # volatility proxy
        ])

    # =====================================================
    # 행동 선택 (policy)
    # =====================================================

    def select_action(self):

        total = sum(self.policy_score.values())

        probs = {
            k: v / total for k, v in self.policy_score.items()
        }

        action = np.random.choice(
            list(probs.keys()),
            p=list(probs.values())
        )

        return action

    # =====================================================
    # reward 계산
    # =====================================================

    def reward(self, pnl):

        # risk-adjusted reward
        return pnl - abs(pnl) * 0.1

    # =====================================================
    # memory 저장
    # =====================================================

    def store(self, state, action, reward):

        self.memory.append((state, action, reward))

    # =====================================================
    # policy update (간단 PPO 스타일 흉내)
    # =====================================================

    def update_policy(self):

        if len(self.memory) < 50:
            return

        rewards = {}

        for state, action, reward in self.memory:

            if action not in rewards:
                rewards[action] = []

            rewards[action].append(reward)

        # 평균 reward 기반 업데이트
        for action in self.policy_score:

            if action in rewards:
                avg = np.mean(rewards[action])

                self.policy_score[action] += self.learning_rate * avg

        # normalize
        total = sum(self.policy_score.values())

        for k in self.policy_score:
            self.policy_score[k] /= total

        self.memory.clear()

    # =====================================================
    # step (핵심)
    # =====================================================

    def step(self, price, pnl):

        state = self.get_state(price)

        action = brain.select_strategy()[0]

        r = self.reward(pnl)

        self.store(state, action, r)

        self.update_policy()

        return {
            "action": action,
            "reward": r,
            "policy": self.policy_score
        }


# =====================================================
# SINGLETON
# =====================================================

rl_engine = RLTradingEngine()
