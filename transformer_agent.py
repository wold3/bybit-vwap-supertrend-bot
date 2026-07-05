import torch
import torch.optim as optim
import random

from model_transformer import TransformerPolicy


class TransformerAgent:

    def __init__(self):

        self.model = TransformerPolicy()
        self.opt = optim.Adam(self.model.parameters(), lr=0.0003)

        self.memory = []

    def act(self, state_seq):

        if random.random() < 0.1:
            return random.randint(0, 2)

        with torch.no_grad():

            x = torch.tensor(state_seq).float().unsqueeze(0)

            logits = self.model(x)

            return int(torch.argmax(logits))

    def train(self, batch_size=32):

        if len(self.memory) < batch_size:
            return

        batch = random.sample(self.memory, batch_size)

        for s, a, r in batch:

            x = torch.tensor(s).float().unsqueeze(0)

            logits = self.model(x)[0]

            loss = (logits[a] - r) ** 2

            self.opt.zero_grad()
            loss.backward()
            self.opt.step()

    def store(self, state_seq, action, reward):

        self.memory.append((state_seq, action, reward))
