import numpy as np


class RiskEngine:

    def __init__(self, alpha=0.05):
        self.returns = []
        self.alpha = alpha

    def update(self, pnl):

        self.returns.append(float(pnl))

        if len(self.returns) > 1000:
            self.returns.pop(0)

    def cvar(self):

        if len(self.returns) < 20:
            return 0.0

        arr = np.array(self.returns)

        var = np.percentile(arr, self.alpha * 100)

        tail = arr[arr <= var]

        if len(tail) == 0:
            return 0.0

        return float(np.mean(tail))

    def risk_penalty(self, pnl):

        return float(pnl) - abs(self.cvar()) * 0.5
