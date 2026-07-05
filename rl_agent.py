import json
import os
import random

from config import GAMMA


class RLAgent:
    """
    Q-Learning Agent
    """

    def __init__(
        self,
        alpha=0.1,
        epsilon=0.1,
        gamma=GAMMA,
        model_path="models/q_table.json",
    ):

        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma

        self.model_path = model_path

        self.q = {}

        self.load()

    # ------------------------------------------------

    def _key(self, state):
        """
        State를 문자열 Key로 변환
        """

        return ",".join(
            f"{float(x):.4f}"
            for x in state
        )

    # ------------------------------------------------

    def act(self, state):
        """
        ε-greedy 정책
        """

        key = self._key(state)

        if key not in self.q:
            self.q[key] = [0.0, 0.0, 0.0]

        # Exploration
        if random.random() < self.epsilon:
            return random.randint(0, 2)

        # Exploitation
        values = self.q[key]

        return values.index(max(values))

    # ------------------------------------------------

    def learn(
        self,
        state,
        action,
        reward,
        next_state,
        done=False,
    ):
        """
        Q-Learning Update
        """

        state_key = self._key(state)
        next_key = self._key(next_state)

        if state_key not in self.q:
            self.q[state_key] = [0.0, 0.0, 0.0]

        if next_key not in self.q:
            self.q[next_key] = [0.0, 0.0, 0.0]

        current_q = self.q[state_key][action]

        if done:
            target = reward
        else:
            target = reward + self.gamma * max(self.q[next_key])

        self.q[state_key][action] = (
            current_q
            + self.alpha * (target - current_q)
        )

    # ------------------------------------------------

    def save(self):

        os.makedirs(
            os.path.dirname(self.model_path),
            exist_ok=True,
        )

        with open(
            self.model_path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                self.q,
                f,
                indent=2,
            )

    # ------------------------------------------------

    def load(self):

        if not os.path.exists(self.model_path):
            return

        try:

            with open(
                self.model_path,
                "r",
                encoding="utf-8",
            ) as f:

                self.q = json.load(f)

        except Exception:

            self.q = {}

    # ------------------------------------------------

    def reset(self):

        self.q = {}

    # ------------------------------------------------

    def size(self):

        return len(self.q)
