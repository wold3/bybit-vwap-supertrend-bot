import random
from collections import deque

from config import REPLAY_BUFFER_SIZE


class ReplayBuffer:
    """
    DQN Experience Replay Buffer
    """

    def __init__(self, size=REPLAY_BUFFER_SIZE):

        self.buffer = deque(maxlen=size)

    # ---------------------------------------------

    def push(
        self,
        state,
        action,
        reward,
        next_state,
        done=False,
    ):
        """
        경험 저장
        """

        self.buffer.append(
            (
                state,
                action,
                reward,
                next_state,
                done,
            )
        )

    # ---------------------------------------------

    def sample(self, batch_size):
        """
        Mini Batch 추출
        """

        batch_size = min(
            batch_size,
            len(self.buffer),
        )

        return random.sample(
            self.buffer,
            batch_size,
        )

    # ---------------------------------------------

    def clear(self):
        """
        버퍼 초기화
        """

        self.buffer.clear()

    # ---------------------------------------------

    def size(self):
        """
        현재 버퍼 크기
        """

        return len(self.buffer)

    # ---------------------------------------------

    def is_empty(self):

        return len(self.buffer) == 0

    # ---------------------------------------------

    def __len__(self):

        return len(self.buffer)
