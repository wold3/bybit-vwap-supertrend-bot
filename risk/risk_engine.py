class Risk:

    def __init__(self):
        self.pnl = 0
        self.trades = 0
        self.enabled = True

    def allow(self):

        if self.pnl <= -50:
            self.enabled = False

        return self.enabled

    def update_pnl(self, pnl):
        self.pnl = pnl

    def add_trade(self):
        self.trades += 1

risk = Risk()
