class PortfolioManager:

    def __init__(self):

        self.positions = {}

    def update(self, symbol, pnl):

        self.positions[symbol] = self.positions.get(symbol, 0) + pnl

    def risk_exposure(self):

        return sum(abs(v) for v in self.positions.values())

    def allow_trade(self):

        return self.risk_exposure() < 1000
