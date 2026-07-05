import torch
import random
import torch.optim as optim

from transformer_policy import TransformerPolicy


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

    def store(self, s, a, r):

        self.memory.append((s, a, r))

    def train(self):

        import random

        if len(self.memory) < 32:
            return

        batch = random.sample(self.memory, 32)

        for s, a, r in batch:

            x = torch.tensor(s).float().unsqueeze(0)

            logits = self.model(x)[0]

            loss = (logits[a] - r) ** 2

            self.opt.zero_grad()
            loss.backward()
            self.opt.step()
