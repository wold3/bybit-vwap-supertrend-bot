import time

from config import (
    ORDER_COOLDOWN,
    MAX_POSITION_SIZE,
    MAX_DAILY_LOSS_PERCENT,
)



# ==========================================
# RISK MANAGER
# ==========================================

class RiskManager:


    def __init__(self):

        self.start_equity = 0

        self.current_equity = 0

        self.last_order_time = 0

        self.daily_loss = 0


        print("==============================")
        print("[RISK MANAGER INIT]")
        print("MAX DAILY LOSS :", MAX_DAILY_LOSS_PERCENT, "%")
        print("ORDER COOLDOWN :", ORDER_COOLDOWN)
        print("==============================")



    # ======================================
    # INITIALIZE
    # ======================================

    def initialize(self, equity=None):


        try:

            if equity is None:

                equity = 0



            self.start_equity = float(equity)

            self.current_equity = float(equity)


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
    # ORDER COOLDOWN CHECK
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

    def check_position_size(self, qty):


        try:


            qty = float(qty)



            if qty > MAX_POSITION_SIZE:


                print(
                    "[RISK BLOCK] POSITION SIZE LIMIT"
                )


                return False



            return True



        except Exception as e:


            print(
                "[POSITION SIZE ERROR]",
                e
            )


            return False




    # ======================================
    # DAILY LOSS CHECK
    # ======================================

    def check_daily_loss(self, equity):


        try:


            self.current_equity = float(equity)



            if self.start_equity <= 0:

                return True



            loss_percent = (

                (
                    self.start_equity
                    -
                    self.current_equity
                )

                /

                self.start_equity

                *

                100

            )



            self.daily_loss = loss_percent



            if loss_percent >= MAX_DAILY_LOSS_PERCENT:


                print(
                    "[RISK BLOCK] DAILY LOSS LIMIT",
                    loss_percent,
                    "%"
                )


                return False



            return True



        except Exception as e:


            print(
                "[LOSS CHECK ERROR]",
                e
            )


            return False




    # ======================================
    # STATUS
    # ======================================

    def status(self):


        return {

            "start_equity":
                self.start_equity,

            "current_equity":
                self.current_equity,

            "daily_loss":
                self.daily_loss,

            "last_order":
                self.last_order_time

        }





# ==========================================
# SINGLETON
# ==========================================

risk_manager = RiskManager()
