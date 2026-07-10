# =====================================================
# risk/risk_manager.py
# Risk Management Engine
# =====================================================


import time
import threading



from config import (
    RISK_PER_TRADE_PERCENT,
    MAX_POSITION_SIZE,
    MAX_DAILY_LOSS_PERCENT,
    MAX_LOSS_STREAK
)







class RiskManager:



    def __init__(self):


        self.lock = threading.Lock()



        self.equity = 0


        self.start_equity = 0


        self.daily_loss = 0


        self.loss_streak = 0


        self.initialized = False



        print(

            "[RISK MANAGER INIT]"

        )









    # =====================================================
    # INITIALIZE
    # =====================================================

    def initialize(
        self,
        equity
    ):


        with self.lock:


            self.equity = float(

                equity

            )


            self.start_equity = float(

                equity

            )


            self.daily_loss = 0


            self.loss_streak = 0


            self.initialized = True




        print(

            "[RISK READY]",

            equity

        )









    # =====================================================
    # CAN TRADE
    # =====================================================

    def can_trade(self):


        try:


            if not self.initialized:


                return False





            # loss streak

            if self.loss_streak >= MAX_LOSS_STREAK:


                print(

                    "[RISK BLOCK] LOSS STREAK"

                )


                return False






            # daily loss


            loss_percent = (


                self.daily_loss

                /

                self.start_equity

            ) * 100





            if loss_percent >= MAX_DAILY_LOSS_PERCENT:


                print(

                    "[RISK BLOCK] DAILY LOSS"

                )


                return False






            return True






        except Exception as e:


            print(

                "[RISK CHECK ERROR]",

                e

            )


            return False











    # =====================================================
    # POSITION SIZE
    # =====================================================

    def calculate_position_size(
        self,
        entry,
        stop
    ):


        try:


            if entry <= 0:


                return 0





            if stop <= 0:


                return 0






            risk_money = (

                self.equity

                *

                (

                    RISK_PER_TRADE_PERCENT

                    /

                    100

                )

            )






            distance = abs(

                entry

                -

                stop

            )





            if distance == 0:


                return 0






            qty = (

                risk_money

                /

                distance

            )





            return qty







        except Exception as e:


            print(

                "[POSITION SIZE ERROR]",

                e

            )


            return 0










    # =====================================================
    # MAX POSITION CHECK
    # =====================================================

    def check_position_size(
        self,
        qty
    ):


        try:



            if qty <= 0:


                return False






            if qty > MAX_POSITION_SIZE:


                print(

                    "[POSITION LIMIT]",

                    qty

                )


                return False






            return True






        except:


            return False











    # =====================================================
    # UPDATE PNL
    # =====================================================

    def update_pnl(
        self,
        pnl
    ):


        with self.lock:



            pnl = float(

                pnl

            )




            self.equity += pnl





            if pnl < 0:


                self.loss_streak += 1


                self.daily_loss += abs(

                    pnl

                )



            else:


                self.loss_streak = 0









    # =====================================================
    # RESET DAILY
    # =====================================================

    def reset_daily(self):


        with self.lock:


            self.daily_loss = 0


            self.loss_streak = 0


            self.start_equity = self.equity





        print(

            "[RISK DAILY RESET]"

        )









    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "equity":

                self.equity,


            "daily_loss":

                self.daily_loss,


            "loss_streak":

                self.loss_streak,


            "can_trade":

                self.can_trade()


        }









# =====================================================
# SINGLETON
# =====================================================

risk_manager = RiskManager()
