import torch
import torch.nn as nn
import torch.optim as optim

from market_encoder import MarketEncoder


class SSLTrainer:

    def __init__(self):

        self.model = MarketEncoder()
        self.opt = optim.Adam(self.model.parameters(), lr=0.001)
        self.loss_fn = nn.CosineEmbeddingLoss()

        self.data = []

    def add(self, seq):
        self.data.append(seq)

        if len(self.data) > 10000:
            self.data.pop(0)

    def sample(self):

        import random

        a = random.choice(self.data)
        b = random.choice(self.data)

        label = 1 if abs(len(a) - len(b)) < 3 else 0

        return a, b, label

    def train_step(self):

        import random

        if len(self.data) < 50:
            return

        for _ in range(16):

            a, b, label = self.sample()

            a = torch.tensor(a).float()
            b = torch.tensor(b).float()

            emb_a = self.model(a)
            emb_b = self.model(b)

            target = torch.tensor(1.0 if label == 1 else -1.0)

            loss = self.loss_fn(emb_a, emb_b, target)

            self.opt.zero_grad()
            loss.backward()
            self.opt.step()
