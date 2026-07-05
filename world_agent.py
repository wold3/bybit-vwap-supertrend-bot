import torch
import random

from world_model import WorldModel


class WorldAgent:

    def __init__(self):

        self.model = WorldModel()

    def imagine(self, state_seq):

        x = torch.tensor(state_seq).float()

        z = self.model.encode(x)

        z_seq = z.unsqueeze(0)

        pred = self.model.predict(z_seq)

        return pred

    def act(self, state_seq):

        if random.random() < 0.1:
            return random.randint(0, 2)

        pred = self.imagine(state_seq)

        score = pred.mean().item()

        if score > 0.1:
            return 1
        elif score < -0.1:
            return 2
        else:
            return 0
