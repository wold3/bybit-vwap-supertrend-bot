import torch
import random
from world_model import WorldModel


class WorldAgent:

    def __init__(self):
        self.model = WorldModel()

    def act(self, state_seq):

        x = torch.tensor(state_seq).float()

        emb = self.model(x).mean().item()

        if random.random() < 0.1:
            return random.randint(0, 2)

        if emb > 0:
            return 1
        elif emb < -0.2:
            return 2
        return 0
