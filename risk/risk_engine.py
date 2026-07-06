import time


class RiskEngine:

    def __init__(self):

        self.start_equity = 10000
        self.current_equity = 10000
        self.peak_equity = 10000

        self.max_drawdown = 10.0   # %
        self.daily_loss_limit = 5.0

        self.trading_halted = False

    # =================================================
    # EQUITY UPDATE
    # =================================================
    def update_equity(self, equity):

        self.current_equity = equity

        if equity > self.peak_equity:
            self.peak_equity = equity

    # =================================================
    # DRAW DOWN CALC
    # =================================================
    def get_drawdown(self):

        if self.peak_equity == 0:
            return 0

        dd = (
            (self.peak_equity - self.current_equity)
            / self.peak_equity
        ) * 100

        return dd

    # =================================================
    # RISK CHECK
    # =================================================
    def can_trade(self):

        dd = self.get_drawdown()

        # ================================
        # MAX DRAWDOWN STOP
        # ================================
        if dd >= self.max_drawdown:
            self.trading_halted = True
            print("[RISK] MAX DRAWDOWN HIT → STOP")
            return False

        # ================================
        # DAILY LOSS STOP
        # ================================
        pnl_pct = (
            (self.current_equity - self.start_equity)
            / self.start_equity
        ) * 100

        if pnl_pct <= -self.daily_loss_limit:
            self.trading_halted = True
            print("[RISK] DAILY LOSS HIT → STOP")
            return False

        return True

    # =================================================
    # STATUS
    # =================================================
    def status(self):

        return {
            "equity": self.current_equity,
            "peak": self.peak_equity,
            "drawdown": self.get_drawdown(),
            "halted": self.trading_halted
        }


# SINGLETON
risk_engine = RiskEngine()
