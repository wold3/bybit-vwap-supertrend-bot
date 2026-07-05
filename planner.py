import torch


class Planner:

    def __init__(self, world_model):
        self.world_model = world_model

    def rollout(self, state_seq, action):

        x = torch.tensor(state_seq).float()

        z = self.world_model.encode(x)
        z_seq = z.unsqueeze(0)

        future = self.world_model.predict(z_seq)

        score = future.mean().item()

        if action == 1:
            return score * 1.1
        elif action == 2:
            return -score * 1.1
        else:
            return score * 0.1

    def plan(self, state_seq):

        actions = [0, 1, 2]

        scores = [self.rollout(state_seq, a) for a in actions]

        return int(torch.tensor(scores).argmax())
