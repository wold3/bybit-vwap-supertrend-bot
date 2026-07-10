import time

from config import (
    DAILY_LOSS_LIMIT,
    MAX_POSITION_SIZE,
)

from api.bybit_api import bybit_api


# ==========================================
# RISK MANAGER
# ==========================================

class RiskManager:


    def __init__(self):

        self.start_equity = self.get_equity()

        self.daily_start_equity = self.start_equity

        self.last_order_time = 0


        print("==============================")
        print("[RISK INIT EQUITY]", self.start_equity)
        print("==============================")


    # ======================================
    # EQUITY
    # ======================================

    def get_equity(self):

        try:

            wallet = bybit_api.get_wallet_balance()


            if not wallet:
                return 0.0


            if wallet.get("retCode") != 0:
                return 0.0


            data = wallet["result"]["list"][0]


            equity = float(
                data.get(
                    "totalEquity",
                    0
                )
            )


            return equity


        except Exception as e:

            print(
                "[EQUITY ERROR]",
                e
            )

            return 0.0



    # ======================================
    # DAILY LOSS CHECK
    # ======================================

    def check_daily_loss(self):

        try:

            current = self.get_equity()


            if self.daily_start_equity <= 0:

                return False



            loss_percent = (

                self.daily_start_equity - current

            ) / self.daily_start_equity



            print(
                "[DAILY LOSS]",
                round(loss_percent * 100, 4),
                "%"
            )


            if loss_percent >= DAILY_LOSS_LIMIT:

                print(
                    "[RISK STOP] DAILY LOSS LIMIT"
                )

                return True



            return False



        except Exception as e:


            print(
                "[DAILY LOSS ERROR]",
                e
            )

            return False



    # ======================================
    # ORDER COOLDOWN
    # ======================================

    def order_allowed(self):

        now = time.time()


        if now - self.last_order_time < 60:

            return False


        return True



    def update_order_time(self):

        self.last_order_time = time.time()



    # ======================================
    # POSITION SIZE
    # ======================================

    def check_position_size(
        self,
        qty
    ):

        if qty > MAX_POSITION_SIZE:

            print(
                "[RISK BLOCK] POSITION SIZE"
            )

            return False


        return True




# ==========================================
# SINGLETON
# ==========================================

risk_manager = RiskManager()
