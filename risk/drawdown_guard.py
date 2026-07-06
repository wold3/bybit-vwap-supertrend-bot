import time


class DrawdownGuard:

    def __init__(self):

        self.peak_equity = 0
        self.current_equity = 0

        self.max_drawdown = 0.05  # 5%

        self.trading_enabled = True

    # =================================================
    # UPDATE EQUITY
    # =================================================
    def update(self, equity):

        self.current_equity = equity

        if equity > self.peak_equity:

            self.peak_equity = equity

        self._check_drawdown()

    # =================================================
    # CALCULATE DD
    # =================================================
    def get_drawdown(self):

        if self.peak_equity == 0:
            return 0

        dd = (self.peak_equity - self.current_equity) / self.peak_equity

        return dd

    # =================================================
    # CHECK RULE
    # =================================================
    def _check_drawdown(self):

        dd = self.get_drawdown()

        print(f"[DD] {dd * 100:.2f}%")

        if dd >= self.max_drawdown:

            self.trading_enabled = False

            print("[RISK] TRADING DISABLED (DRAWDOWN LIMIT)")

    # =================================================
    # ALLOW TRADE?
    # =================================================
    def can_trade(self):

        return self.trading_enabled


# SINGLETON
drawdown_guard = DrawdownGuard()
