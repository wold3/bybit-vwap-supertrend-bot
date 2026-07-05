import random

import torch
import torch.nn.functional as F
import torch.optim as optim

from config import (
    LEARNING_RATE,
    GAMMA,
    EPSILON,
    EPSILON_MIN,
    EPSILON_DECAY,
    TARGET_UPDATE,
    MODEL_PATH,
)
from dqn_model import DQN
from replay_buffer import ReplayBuffer


class Agent:

    def __init__(self):

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.model = DQN().to(self.device)

        self.target = DQN().to(self.device)
        self.target.load_state_dict(
            self.model.state_dict()
        )

        self.optimizer = optim.Adam(
            self.model.parameters(),
            lr=LEARNING_RATE,
        )

        self.buffer = ReplayBuffer()

        self.gamma = GAMMA

        self.epsilon = EPSILON
        self.epsilon_min = EPSILON_MIN
        self.epsilon_decay = EPSILON_DECAY

        self.update_count = 0

    # ------------------------------------------------

    def act(self, state):

        if random.random() < self.epsilon:
            return random.randint(0, 2)

        state = torch.tensor(
            state,
            dtype=torch.float32,
            device=self.device,
        )

        with torch.no_grad():

            q = self.model(state)

            return int(torch.argmax(q).item())

    # ------------------------------------------------

    def remember(
        self,
        state,
        action,
        reward,
        next_state,
        done=False,
    ):

        self.buffer.push(
            state,
            action,
            reward,
            next_state,
            done,
        )

    # ------------------------------------------------

    def train(self, batch_size=32):

        if len(self.buffer) < batch_size:
            return None

        batch = self.buffer.sample(batch_size)

        losses = []

        for (
            state,
            action,
            reward,
            next_state,
            done,
        ) in batch:

            state = torch.tensor(
                state,
                dtype=torch.float32,
                device=self.device,
            )

            next_state = torch.tensor(
                next_state,
                dtype=torch.float32,
                device=self.device,
            )

            q = self.model(state)[action]

            with torch.no_grad():

                next_q = self.target(next_state).max()

                target = reward

                if not done:
                    target += self.gamma * next_q

            loss = F.mse_loss(q, target)

            self.optimizer.zero_grad()

            loss.backward()

            self.optimizer.step()

            losses.append(loss.item())

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        self.update_count += 1

        if self.update_count % TARGET_UPDATE == 0:
            self.update_target()

        return sum(losses) / len(losses)

    # ------------------------------------------------

    def update_target(self):

        self.target.load_state_dict(
            self.model.state_dict()
        )

    # ------------------------------------------------

    def save(self, path=MODEL_PATH):

        torch.save(
            self.model.state_dict(),
            path,
        )

    # ------------------------------------------------

    def load(self, path=MODEL_PATH):

        self.model.load_state_dict(
            torch.load(
                path,
                map_location=self.device,
            )
        )

        self.update_target()
