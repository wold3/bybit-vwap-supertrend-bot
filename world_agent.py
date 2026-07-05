from world_model import WorldModel
from planner import Planner


class WorldAgent:

    def __init__(self):

        self.model = WorldModel()
        self.planner = Planner(self.model)

    def act(self, state_seq):

        return self.planner.plan(state_seq)
