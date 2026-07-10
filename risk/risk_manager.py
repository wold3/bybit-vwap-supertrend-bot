import time


from config import (
    MAX_DAILY_LOSS_PERCENT,
    MAX_POSITION_SIZE,
)





# ==========================================
# RISK MANAGER
# ==========================================

class RiskManager:


    def __init__(self):


        self.start_equity = 0


        self.current_equity = 0


        self.initialized = False


        self.daily_loss_limit = (

            MAX_DAILY_LOSS_PERCENT

        )



        print("==============================")
        print("[RISK MANAGER INIT]")
        print(
            "MAX DAILY LOSS :",
            self.daily_loss_limit,
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


            self.initialized = True



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



        except:


            pass





    # ======================================
    # LOSS PERCENT
    # ======================================

    def loss_percent(self):


        if self.start_equity <= 0:


            return 0




        loss = (

            self.start_equity

            -

            self.current_equity

        )



        return (

            loss

            /

            self.start_equity

        ) * 100





    # ======================================
    # TRADE CHECK
    # ======================================

    def can_trade(self):


        if not self.initialized:


            print(
                "[RISK BLOCK] NOT INITIALIZED"
            )


            return False





        loss = self.loss_percent()





        if loss >= self.daily_loss_limit:



            print(
                "[RISK BLOCK]"
            )


            print(
                "LOSS :",
                round(loss,2),
                "%"
            )


            return False





        return True





    # ======================================
    # POSITION SIZE CHECK
    # ======================================

    def check_position_size(

        self,

        qty

    ):


        try:


            qty = float(qty)



            if qty > MAX_POSITION_SIZE:


                print(
                    "[RISK BLOCK] POSITION SIZE"
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
    # STATUS
    # ======================================

    def status(self):


        return {


            "start_equity":

                self.start_equity,


            "current_equity":

                self.current_equity,


            "loss_percent":

                self.loss_percent(),


            "can_trade":

                self.can_trade()

        }





# ==========================================
# SINGLETON
# ==========================================

risk_manager = RiskManager()
