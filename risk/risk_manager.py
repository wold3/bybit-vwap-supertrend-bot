import time


from config import (
    MAX_POSITION_SIZE,
    DAILY_LOSS_LIMIT,
    ORDER_COOLDOWN,
)


from portfolio.bybit_wallet import (
    wallet,
)


from position.position_manager import (
    position_manager,
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


        self.daily_loss_limit = (

            DAILY_LOSS_LIMIT

        )



        self.last_order_time = 0



        self.start_equity = None




        print("==============================")
        print("[RISK MANAGER READY]")
        print("==============================")









    # =====================================================
    # INIT
    # =====================================================

    def initialize(self):


        try:


            equity = wallet.get_equity()



            self.start_equity = float(

                equity

            )



            print(
                "[RISK INIT EQUITY]",
                self.start_equity
            )




        except Exception as e:


            print(
                "[RISK INIT ERROR]",
                e
            )









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



        except:


            print(
                "[RISK BLOCK] INVALID QTY"
            )


            return False








        if qty <= 0:


            print(
                "[RISK BLOCK] ZERO SIZE"
            )


            return False








        if qty > self.max_position_size:


            print(
                "[RISK BLOCK] MAX SIZE"
            )


            return False







        # 현재 포지션 확인

        position_manager.sync()



        if position_manager.has_position():


            print(
                "[RISK BLOCK] POSITION EXISTS"
            )


            return False







        # cooldown


        elapsed = (

            time.time()

            -

            self.last_order_time

        )



        if elapsed < self.cooldown_seconds:


            remain = round(

                self.cooldown_seconds

                -

                elapsed,

                1

            )


            print(

                "[RISK BLOCK] COOLDOWN",

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


        if self.start_equity is None:


            return True






        try:


            current = float(

                wallet.get_equity()

            )



            pnl = (

                current

                -

                self.start_equity

            )



            print(

                "[DAILY PNL]",

                round(pnl,2)

            )





            if pnl <= self.daily_loss_limit:


                print(

                    "[RISK STOP] DAILY LOSS LIMIT",

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



        except:


            pass






        return {


            "enabled":

                self.enabled,


            "max_position":

                self.max_position_size,


            "cooldown":

                self.cooldown_seconds,


            "daily_loss_limit":

                self.daily_loss_limit,


            "start_equity":

                self.start_equity,


            "current_pnl":

                pnl,


        }











risk_manager = RiskManager()
