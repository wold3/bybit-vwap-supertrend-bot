import datetime


class RiskEngine:

    def __init__(self):

        self.pnl = 0
        self.trades = 0
        self.enabled = True
        self.day = datetime.date.today()

    def reset(self):

        self.pnl = 0
        self.trades = 0
        self.enabled = True
        self.day = datetime.date.today()

    def check_reset(self):

        if self.day != datetime.date.today():
            self.reset()

    def allow_trade(self):

        self.check_reset()

        if not self.enabled:
            return False

        if self.pnl <= -50:
            self.enabled = False
            return False

        if self.trades >= 20:
            return False

        return True

    def update_pnl(self, pnl):
        self.pnl += pnl

    def add_trade(self):
        self.trades += 1


risk_engine = RiskEngine()
