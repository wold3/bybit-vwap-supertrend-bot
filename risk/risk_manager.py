import time

from config import (
    ORDER_COOLDOWN,
    DEFAULT_QTY,
)


# ==========================================
# RISK MANAGER
# ==========================================

class RiskManager:


    def __init__(self):

        self.last_order_time = 0

        self.initial_equity = 0

        self.current_equity = 0

        self.max_daily_loss = 5.0   # %

        self.daily_loss = 0


        print("==============================")
        print("[RISK MANAGER INIT]")
        print("ORDER COOLDOWN :", ORDER_COOLDOWN)
        print("MAX DAILY LOSS :", self.max_daily_loss, "%")
        print("==============================")



    # ======================================
    # INITIALIZE
    # ======================================

    def initialize(
        self,
        equity
    ):

        try:

            self.initial_equity = float(equity)

            self.current_equity = float(equity)


            print("==============================")
            print("[RISK INITIALIZED]")
            print("INIT EQUITY :", self.initial_equity)
            print("==============================")


            return True


        except Exception as e:

            print(
                "[RISK INIT ERROR]",
                e
            )

            return False



    # ======================================
    # UPDATE EQUITY
    # ======================================

    def update_equity(
        self,
        equity
    ):

        try:

            self.current_equity = float(equity)


            if self.initial_equity > 0:

                loss = (
                    self.initial_equity
                    -
                    self.current_equity
                )


                self.daily_loss = (
                    loss
                    /
                    self.initial_equity
                ) * 100



            print(
                "[DAILY LOSS]",
                round(
                    self.daily_loss,
                    4
                ),
                "%"
            )


        except Exception as e:

            print(
                "[EQUITY UPDATE ERROR]",
                e
            )



    # ======================================
    # DAILY LOSS CHECK
    # ======================================

    def daily_loss_allowed(self):


        if self.daily_loss >= self.max_daily_loss:


            print(
                "[RISK BLOCK] DAILY LOSS LIMIT"
            )


            return False


        return True




    # ======================================
    # ORDER COOLDOWN CHECK
    # ======================================

    def order_allowed(self):


        now = time.time()


        elapsed = (
            now
            -
            self.last_order_time
        )


        if elapsed < ORDER_COOLDOWN:


            remain = (
                ORDER_COOLDOWN
                -
                elapsed
            )


            print(
                "[COOLDOWN]",
                round(remain,1),
                "sec"
            )


            return False



        if not self.daily_loss_allowed():

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



            max_qty = float(DEFAULT_QTY) * 10



            if qty > max_qty:


                print(
                    "[RISK BLOCK] POSITION TOO LARGE"
                )

                print(
                    "MAX :",
                    max_qty
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
    # MANUAL RESET
    # ======================================

    def reset_daily_loss(self):

        self.daily_loss = 0

        self.initial_equity = self.current_equity



    # ======================================
    # STATUS
    # ======================================

    def status(self):

        return {

            "initial_equity":
                self.initial_equity,

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
