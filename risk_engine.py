import numpy as np


class RiskEngine:

    def __init__(self):

        self.pnl_history = []

    def update(self, pnl):

        self.pnl_history.append(float(pnl))

        if len(self.pnl_history) > 1000:
            self.pnl_history.pop(0)

    def cvar(self):

        if len(self.pnl_history) < 20:
            return 0.0

        arr = np.array(self.pnl_history)

        var = np.percentile(arr, 5)

        tail = arr[arr <= var]

        return float(tail.mean()) if len(tail) else 0.0
