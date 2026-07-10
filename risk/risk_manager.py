import time

from config import (
    MAX_DAILY_LOSS_PERCENT,
    ORDER_COOLDOWN,
    MAX_POSITION_SIZE,
)



# ==========================================
# RISK MANAGER
# ==========================================

class RiskManager:


    def __init__(self):


        self.start_equity = 0

        self.current_equity = 0

        self.daily_loss = 0


        self.last_order_time = 0


        print("==============================")
        print("[RISK MANAGER INIT]")
        print(
            "MAX DAILY LOSS :",
            MAX_DAILY_LOSS_PERCENT,
            "%"
        )
        print(
            "ORDER COOLDOWN :",
            ORDER_COOLDOWN
        )
        print("==============================")




    # ======================================
    # INITIALIZE
    # ======================================

    def initialize(
        self,
        equity=0
    ):


        try:


            self.start_equity = float(
                equity
            )


            self.current_equity = float(
                equity
            )


            self.daily_loss = 0



            print("==============================")
            print("[RISK INITIALIZED]")
            print(
                "START EQUITY :",
                self.start_equity
            )
            print("==============================")



        except Exception as e:


            print(
                "[RISK INIT ERROR]",
                e
            )





    # ======================================
    # UPDATE EQUITY
    # ======================================

    def update_equity(
        self,
        equity
    ):


        self.current_equity = float(
            equity
        )



        self.daily_loss = (

            (
                self.start_equity
                -
                self.current_equity
            )
            /
            self.start_equity

        ) * 100





    # ======================================
    # DAILY LOSS CHECK
    # ======================================

    def allow_trade(self):


        if self.start_equity <= 0:

            return False



        if self.daily_loss >= MAX_DAILY_LOSS_PERCENT:


            print(
                "[RISK BLOCK]",
                "DAILY LOSS LIMIT"
            )


            return False



        return True




    # ======================================
    # ORDER COOLDOWN
    # ======================================

    def check_cooldown(self):


        now = time.time()



        if (

            now - self.last_order_time

            <
            
            ORDER_COOLDOWN

        ):


            remain = int(

                ORDER_COOLDOWN

                -

                (
                    now
                    -
                    self.last_order_time
                )

            )


            print(
                "[COOLDOWN]",
                remain,
                "sec"
            )


            return False



        return True




    # ======================================
    # ORDER REGISTER
    # ======================================

    def register_order(self):


        self.last_order_time = time.time()




    # ======================================
    # POSITION SIZE CHECK
    # ======================================

    def check_position_size(
        self,
        qty
    ):


        if float(qty) > MAX_POSITION_SIZE:


            print(
                "[RISK BLOCK]",
                "POSITION SIZE"
            )


            return False



        return True





# ==========================================
# SINGLETON
# ==========================================

risk_manager = RiskManager()
