class PortfolioAgent:

    def __init__(self):

        self.symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]

        self.base_alloc = {
            "BTCUSDT": 0.4,
            "ETHUSDT": 0.3,
            "SOLUSDT": 0.3,
        }

    def get_weights(self, signals):

        total = sum(abs(v) for v in signals.values())

        if total == 0:
            return {s: 0 for s in signals}

        return {
            s: signals[s] / total
            for s in signals
        }
