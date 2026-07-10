import datetime


from config import (
    MAX_DAILY_LOSS_PERCENT,
)



# ==========================================
# RISK MANAGER
# ==========================================

class RiskManager:


    def __init__(self):


        self.start_equity = 0

        self.current_equity = 0


        self.start_time = None


        self.block_trading = False



        print("==============================")
        print("[RISK MANAGER INIT]")
        print(
            "MAX DAILY LOSS :",
            MAX_DAILY_LOSS_PERCENT,
            "%"
        )
        print("==============================")





    # ======================================
    # INITIALIZE
    # ======================================

    def initialize(self, equity):


        try:


            self.start_equity = float(
                equity
            )


            self.current_equity = float(
                equity
            )


            self.start_time = datetime.datetime.now()



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

    def update_equity(self, equity):


        try:


            self.current_equity = float(
                equity
            )



        except Exception as e:


            print(
                "[EQUITY UPDATE ERROR]",
                e
            )





    # ======================================
    # LOSS CHECK
    # ======================================

    def check_daily_loss(self):


        try:


            if self.start_equity <= 0:

                return False




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




            if loss_percent >= MAX_DAILY_LOSS_PERCENT:



                self.block_trading = True



                print(
                    "[RISK BLOCK]",
                    "LOSS:",
                    round(loss_percent,2),
                    "%"
                )



                return True




            return False




        except Exception as e:


            print(
                "[LOSS CHECK ERROR]",
                e
            )


            return False





    # ======================================
    # CAN TRADE
    # ======================================

    def can_trade(self):


        if self.block_trading:


            print(
                "[TRADE BLOCKED BY RISK]"
            )


            return False




        if self.check_daily_loss():


            return False




        return True





    # ======================================
    # RESET
    # ======================================

    def reset(self):


        self.block_trading = False


        self.start_equity = self.current_equity



        print(
            "[RISK RESET]"
        )





# ==========================================
# SINGLETON
# ==========================================

risk_manager = RiskManager()
