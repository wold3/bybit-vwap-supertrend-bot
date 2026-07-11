# =====================================================
# risk/risk_manager.py
# Risk Management System
# =====================================================

import math


from config import (
    RISK_PER_TRADE_PERCENT,
    STOP_LOSS_PERCENT,
    MAX_POSITION_SIZE,
    LEVERAGE,
    DEFAULT_SYMBOL
)





class RiskManager:


    def __init__(self):


        self.equity = 0


        print(

            "[RISK MANAGER INIT]"

        )









    # =====================================================
    # UPDATE EQUITY
    # =====================================================


    def update_equity(
        self,
        equity
    ):


        try:


            self.equity = float(

                equity

            )


            print(

                "[EQUITY UPDATED]",

                self.equity

            )



        except Exception as e:


            print(

                "[EQUITY ERROR]",

                e

            )









    # =====================================================
    # RISK AMOUNT
    # =====================================================


    def risk_amount(self):


        return (

            self.equity

            *

            RISK_PER_TRADE_PERCENT

            /

            100

        )









    # =====================================================
    # POSITION SIZE
    # =====================================================


    def calculate_qty(
        self,
        price
    ):


        try:


            if price <= 0:


                return 0





            risk_money = (

                self.risk_amount()

            )





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

                risk_money

                /

                stop_distance

            )





            # leverage 적용

            qty = qty * LEVERAGE





            # 최대 제한

            if qty > MAX_POSITION_SIZE:


                qty = MAX_POSITION_SIZE





            return round(

                qty,

                6

            )







        except Exception as e:


            print(

                "[QTY ERROR]",

                e

            )


            return 0







    # =====================================================
    # RISK CHECK
    # =====================================================


    def check(
        self,
        price
    ):


        qty = (

            self.calculate_qty(

                price

            )

        )



        if qty <= 0:


            print(

                "[RISK BLOCK]"

            )


            return None





        return {


            "symbol":

                DEFAULT_SYMBOL,


            "qty":

                qty,


            "risk":

                self.risk_amount()

        }









    # =====================================================
    # TP / SL CALCULATION
    # =====================================================


    def calculate_tp_sl(
        self,
        side,
        entry
    ):


        tp_percent = 2.0


        sl_percent = STOP_LOSS_PERCENT





        if side == "Buy":


            tp = (

                entry

                *

                (

                    1

                    +

                    tp_percent

                    /

                    100

                )

            )


            sl = (

                entry

                *

                (

                    1

                    -

                    sl_percent

                    /

                    100

                )

            )





        else:


            tp = (

                entry

                *

                (

                    1

                    -

                    tp_percent

                    /

                    100

                )

            )


            sl = (

                entry

                *

                (

                    1

                    +

                    sl_percent

                    /

                    100

                )

            )





        return {


            "tp":

                round(

                    tp,

                    2

                ),


            "sl":

                round(

                    sl,

                    2

                )

        }









# =====================================================
# INSTANCE
# =====================================================


risk_manager = RiskManager()
