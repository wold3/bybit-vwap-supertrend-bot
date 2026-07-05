import torch
import torch.nn as nn
import torch.optim as optim

from world_model import WorldModel


class ImaginationTrainer:

    def __init__(self):

        self.model = WorldModel()
        self.opt = optim.Adam(self.model.parameters(), lr=0.001)

        self.buffer = []

    def push(self, z_seq):

        self.buffer.append(z_seq)

        if len(self.buffer) > 10000:
            self.buffer.pop(0)

    def train_step(self):

        if len(self.buffer) < 32:
            return

        batch = self.buffer[:32]

        loss_fn = nn.MSELoss()

        for z_seq in batch:

            x = torch.tensor(z_seq).float()

            pred = self.model.predict(x)

            loss = loss_fn(pred, x)

            self.opt.zero_grad()
            loss.backward()
            self.opt.step()
