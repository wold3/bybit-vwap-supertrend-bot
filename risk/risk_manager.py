# =====================================================
# risk/risk_manager.py
# Risk Manager
# =====================================================

import math



from config import (
    RISK_PER_TRADE_PERCENT,
    STOP_LOSS_PERCENT,
    MAX_POSITION_SIZE
)





class RiskManager:



    def __init__(self):


        self.equity = 0


        self.risk_amount = 0


        print(

            "[RISK MANAGER INIT]"

        )









    # =====================================================
    # SET EQUITY
    # =====================================================

    def update_equity(
        self,
        equity
    ):


        try:


            self.equity = float(

                equity

            )



            self.risk_amount = (

                self.equity

                *

                RISK_PER_TRADE_PERCENT

                /

                100

            )



            print(

                "[RISK READY]",

                self.equity

            )



            return True





        except Exception as e:


            print(

                "[RISK EQUITY ERROR]",

                e

            )


            return False










    # =====================================================
    # POSITION SIZE
    # =====================================================

    def calculate_position_size(
        self,
        price
    ):


        try:


            if self.equity <= 0:


                return 0






            stop_distance = (

                price

                *

                STOP_LOSS_PERCENT

                /

                100

            )



            if stop_distance <= 0:


                return 0






            qty = (

                self.risk_amount

                /

                stop_distance

            )







            if qty > MAX_POSITION_SIZE:


                qty = MAX_POSITION_SIZE






            return self.round_qty(

                qty

            )






        except Exception as e:


            print(

                "[POSITION SIZE ERROR]",

                e

            )


            return 0










    # =====================================================
    # QTY ROUND
    # =====================================================

    def round_qty(
        self,
        qty
    ):


        step = 0.001



        qty = math.floor(

            qty / step

        ) * step



        return round(

            qty,

            3

        )









    # =====================================================
    # CHECK RISK
    # =====================================================

    def check_trade(
        self,
        price
    ):


        qty = self.calculate_position_size(

            price

        )



        if qty <= 0:


            print(

                "[RISK BLOCK]"

            )


            return False





        return True










    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "equity":

                self.equity,


            "risk_amount":

                self.risk_amount


        }









# =====================================================
# SINGLETON
# =====================================================

risk_manager = RiskManager()
