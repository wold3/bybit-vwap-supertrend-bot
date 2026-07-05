import torch
import torch.optim as optim
import random

from dqn_model import DQN
from replay_buffer import ReplayBuffer

class Agent:

    def __init__(self):

        self.model = DQN()
        self.target = DQN()
        self.target.load_state_dict(self.model.state_dict())

        self.opt = optim.Adam(self.model.parameters(), lr=0.001)

        self.buffer = ReplayBuffer()

        self.gamma = 0.99

    def act(self, state):

        if random.random() < 0.1:
            return random.randint(0, 2)

        with torch.no_grad():
            q = self.model(torch.tensor(state).float())
            return int(torch.argmax(q))

    def train(self, batch_size=32):

        if len(self.buffer) < batch_size:
            return

        batch = self.buffer.sample(batch_size)

        for s, a, r, s2 in batch:

            s = torch.tensor(s).float()
            s2 = torch.tensor(s2).float()

            q = self.model(s)[a]
            q_next = self.target(s2).max()

            target = r + self.gamma * q_next

            loss = (q - target) ** 2

            self.opt.zero_grad()
            loss.backward()
            self.opt.step()

    def update_target(self):
        self.target.load_state_dict(self.model.state_dict())
