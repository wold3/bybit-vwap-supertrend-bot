import os


class PositionSizer:

    def __init__(self):

        self.risk_per_trade = float(os.getenv("RISK_PER_TRADE", 0.01))  # 1%

    # =================================================
    # CALCULATE POSITION SIZE
    # =================================================
    def calculate(self, balance, entry_price, stop_loss_price):

        risk_amount = balance * self.risk_per_trade

        stop_distance = abs(entry_price - stop_loss_price)

        if stop_distance == 0:
            return 0

        qty = risk_amount / stop_distance

        print(f"[SIZER] qty={qty}")

        return round(qty, 6)


# SINGLETON
position_sizer = PositionSizer()
