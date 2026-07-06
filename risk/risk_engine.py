import datetime

class RiskEngine:

    def __init__(self):

        self.daily_pnl = 0
        self.trade_count = 0
        self.enabled = True
        self.last_reset = datetime.date.today()

    def reset_if_new_day(self):

        if datetime.date.today() != self.last_reset:
            self.daily_pnl = 0
            self.trade_count = 0
            self.last_reset = datetime.date.today()
            self.enabled = True

    def allow_trade(self):

        self.reset_if_new_day()

        if not self.enabled:
            return False

        if self.daily_pnl < -50:
            self.enabled = False
            return False

        if self.trade_count >= 20:
            return False

        return True

    def update(self, pnl):
        self.daily_pnl += pnl

    def add_trade(self):
        self.trade_count += 1


risk_engine = RiskEngine()
