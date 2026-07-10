import time

from config import (
    ORDER_COOLDOWN,
    DEFAULT_QTY,
)

from api.bybit_api import bybit_api


# ==========================================
# RISK MANAGER
# ==========================================

class RiskManager:


    def __init__(self):

        self.start_equity = 0

        self.last_order_time = 0

        self.max_daily_loss = 5.0   # %

        self.current_equity = 0


        print("==============================")
        print("[RISK MANAGER INIT]")
        print("MAX DAILY LOSS :", self.max_daily_loss, "%")
        print("ORDER COOLDOWN :", ORDER_COOLDOWN)
        print("==============================")



    # ======================================
    # INITIALIZE
    # ======================================

    def initialize(self):

        try:

            wallet = bybit_api.get_wallet_balance()


            if wallet:

                self.start_equity = self.get_equity(
                    wallet
                )

                self.current_equity = self.start_equity


            print("==============================")
            print("[RISK INITIALIZED]")
            print("START EQUITY :", self.start_equity)
            print("==============================")


            return True



        except Exception as e:

            print(
                "[RISK INIT ERROR]",
                e
            )

            return False




    # ======================================
    # GET EQUITY
    # ======================================

    def get_equity(
        self,
        wallet=None
    ):


        try:


            if wallet is None:

                wallet = bybit_api.get_wallet_balance()



            value = wallet["result"]["list"][0]["totalEquity"]


            return float(value)



        except Exception as e:


            print(
                "[EQUITY ERROR]",
                e
            )

            return 0




    # ======================================
    # DAILY LOSS CHECK
    # ======================================

    def check_daily_loss(self):


        self.current_equity = self.get_equity()


        if self.start_equity <= 0:

            return True



        loss = (

            self.start_equity
            -
            self.current_equity

        ) / self.start_equity * 100



        print(
            "[DAILY LOSS]",
            round(loss,4),
            "%"
        )



        if loss >= self.max_daily_loss:

            print(
                "[RISK STOP] DAILY LOSS LIMIT"
            )

            return False



        return True




    # ======================================
    # ORDER COOLDOWN
    # ======================================

    def order_allowed(self):


        now = time.time()


        elapsed = now - self.last_order_time



        if elapsed < ORDER_COOLDOWN:

            return False



        return True




    # ======================================
    # UPDATE ORDER TIME
    # ======================================

    def update_order_time(self):

        self.last_order_time = time.time()




    # ======================================
    # POSITION SIZE CHECK
    # ======================================

    def check_position_size(
        self,
        qty
    ):


        try:


            qty = float(qty)



            if qty <= 0:

                print(
                    "[RISK BLOCK] INVALID QTY"
                )

                return False



            if qty > DEFAULT_QTY * 10:

                print(
                    "[RISK BLOCK] TOO LARGE"
                )

                return False



            return True



        except:


            return False




    # ======================================
    # GLOBAL RISK CHECK
    # ======================================

    def allowed(self):


        if not self.check_daily_loss():

            return False



        return True





# ==========================================
# SINGLETON
# ==========================================

risk_manager = RiskManager()
