import time


from config import (
    DEFAULT_SYMBOL
)


from portfolio.bybit_wallet import wallet


from position.position_manager import position_manager






class RiskManager:


    def __init__(self):


        self.enabled = True


        # 최대 계약 수량
        self.max_position_size = 0.01


        # 주문 최소 간격
        self.cooldown_seconds = 30


        self.last_order_time = 0



        # 하루 손실 제한
        self.daily_loss_limit = -100



        self.start_equity = None



        print(
            "[RISK MANAGER READY]"
        )








    # ==========================
    # INIT EQUITY
    # ==========================


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







    # ==========================
    # ORDER CHECK
    # ==========================


    def allow_order(
            self,
            qty
    ):


        if not self.enabled:


            print(
                "[RISK BLOCK] DISABLED"
            )

            return False






        # ----------------------
        # quantity
        # ----------------------


        try:

            qty = float(qty)

        except:


            print(
                "[RISK BLOCK] INVALID QTY"
            )

            return False






        if qty > self.max_position_size:


            print(
                "[RISK BLOCK] MAX SIZE"
            )


            return False







        # ----------------------
        # existing position
        # ----------------------


        try:


            if position_manager.has_position():


                print(
                    "[RISK BLOCK] POSITION EXISTS"
                )


                return False



        except:


            pass







        # ----------------------
        # cooldown
        # ----------------------


        now = time.time()



        if now - self.last_order_time < self.cooldown_seconds:



            print(
                "[RISK BLOCK] COOLDOWN"
            )


            return False






        return True







    # ==========================
    # ORDER SUCCESS
    # ==========================


    def record_order(self):


        self.last_order_time = time.time()



    # ==========================
    # LOSS CHECK
    # ==========================


    def check_daily_loss(self):


        if self.start_equity is None:


            return True






        try:


            current = float(

                wallet.get_equity()

            )



            pnl = current - self.start_equity




            if pnl <= self.daily_loss_limit:


                print(
                    "[RISK STOP] DAILY LOSS",
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







    # ==========================
    # STATUS
    # ==========================


    def status(self):


        return {


            "enabled":

            self.enabled,


            "max_position":

            self.max_position_size,


            "cooldown":

            self.cooldown_seconds,


            "start_equity":

            self.start_equity


        }







risk_manager = RiskManager()
