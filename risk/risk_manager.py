import time


from portfolio.bybit_wallet import wallet

from position.position_manager import position_manager


from config import (
    MAX_POSITION_SIZE,
    DAILY_LOSS_LIMIT,
    ORDER_COOLDOWN,
)





class RiskManager:


    def __init__(self):


        self.enabled = True



        self.max_position_size = (
            MAX_POSITION_SIZE
        )



        self.cooldown_seconds = (
            ORDER_COOLDOWN
        )



        self.last_order_time = 0



        self.daily_loss_limit = (
            DAILY_LOSS_LIMIT
        )



        self.start_equity = None



        self.initialized = False



        print("==============================")
        print("[RISK MANAGER READY]")
        print("==============================")







    # =====================================================
    # INIT
    # =====================================================


    def initialize(self):


        try:



            equity = wallet.get_equity()



            if equity is None:


                print(
                    "[RISK INIT FAILED]"
                )


                return False





            self.start_equity = float(
                equity
            )



            self.initialized = True



            print(

                "[RISK INIT EQUITY]",

                self.start_equity

            )



            return True





        except Exception as e:


            print(
                "[RISK INIT ERROR]",
                e
            )


            return False







    # =====================================================
    # ORDER CHECK
    # =====================================================


    def allow_order(
        self,
        qty
    ):



        if not self.enabled:


            print(
                "[RISK BLOCK] DISABLED"
            )


            return False





        try:


            qty = float(qty)



        except Exception:


            print(
                "[RISK BLOCK] INVALID QTY"
            )


            return False





        if qty <= 0:


            return False





        if qty > self.max_position_size:


            print(
                "[RISK BLOCK] MAX SIZE"
            )


            return False





        # -------------------------
        # Existing Position
        # -------------------------


        try:


            position_manager.sync()



            if position_manager.has_position():


                print(
                    "[RISK BLOCK] POSITION EXISTS"
                )


                return False





        except Exception as e:


            print(
                "[POSITION CHECK ERROR]",
                e
            )








        # -------------------------
        # Cooldown
        # -------------------------


        now = time.time()



        if (

            now - self.last_order_time

            <

            self.cooldown_seconds

        ):


            remain = round(

                self.cooldown_seconds

                -

                (

                    now

                    -

                    self.last_order_time

                ),

                1

            )



            print(

                "[RISK COOLDOWN]",

                remain

            )


            return False






        return True







    # =====================================================
    # RECORD
    # =====================================================


    def record_order(self):


        self.last_order_time = time.time()







    # =====================================================
    # DAILY LOSS
    # =====================================================


    def check_daily_loss(self):


        if not self.initialized:


            return True





        try:


            current = wallet.get_equity()



            if current is None:


                return True





            current = float(
                current
            )



            pnl = (

                current

                -

                self.start_equity

            )





            print(

                "[DAILY PNL]",

                round(
                    pnl,
                    2
                )

            )






            if pnl <= self.daily_loss_limit:



                print(

                    "[RISK STOP]",

                    "LOSS LIMIT",

                    pnl

                )



                self.enabled = False



                return False






        except Exception as e:



            print(

                "[LOSS CHECK ERROR]",

                e

            )



        return True







    # =====================================================
    # RESET
    # =====================================================


    def reset_daily(self):


        self.enabled = True


        self.last_order_time = 0


        self.initialize()



        print(
            "[RISK RESET]"
        )








    # =====================================================
    # STATUS
    # =====================================================


    def status(self):


        pnl = None



        try:


            if self.start_equity:


                pnl = (

                    float(
                        wallet.get_equity()
                    )

                    -

                    self.start_equity

                )



        except Exception:


            pass






        return {


            "enabled":

                self.enabled,


            "max_position":

                self.max_position_size,


            "cooldown":

                self.cooldown_seconds,


            "start_equity":

                self.start_equity,


            "daily_loss_limit":

                self.daily_loss_limit,


            "pnl":

                pnl,


        }






risk_manager = RiskManager()
