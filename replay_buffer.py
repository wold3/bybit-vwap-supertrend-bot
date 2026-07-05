import random
from collections import deque

class ReplayBuffer:

    def __init__(self, size=5000):
        self.buffer = deque(maxlen=size)

    def push(self, s, a, r, s2):
        self.buffer.append((s, a, r, s2))

    def sample(self, n):
        return random.sample(self.buffer, n)

    def __len__(self):
        return len(self.buffer)
