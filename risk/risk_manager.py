# =====================================================
# risk/risk_manager.py
# Risk Management System
# =====================================================

from config import (
    RISK_PER_TRADE_PERCENT,
    STOP_LOSS_PERCENT,
    TAKE_PROFIT_PERCENT,
    MAX_POSITION_SIZE
)





class RiskManager:


    def __init__(self):


        self.equity = 0


        print(

            "[RISK MANAGER READY]"

        )









    # =====================================================
    # UPDATE EQUITY
    # =====================================================


    def update_equity(
        self,
        equity
    ):


        self.equity = float(

            equity

        )


        print(

            "[EQUITY UPDATED]",

            self.equity

        )









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





            risk_money = (

                self.equity

                *

                RISK_PER_TRADE_PERCENT

                /

                100

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





            if qty > MAX_POSITION_SIZE:


                qty = MAX_POSITION_SIZE





            return round(

                qty,

                6

            )






        except Exception as e:


            print(

                "[SIZE ERROR]",

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


        qty = self.calculate_position_size(

            price

        )



        if qty <= 0:


            print(

                "[RISK BLOCK]"

            )


            return None





        return {


            "qty":

                qty,


            "risk":

                RISK_PER_TRADE_PERCENT


        }









    # =====================================================
    # TP / SL
    # =====================================================


    def calculate_tp_sl(
        self,
        side,
        price
    ):


        if side == "Buy":


            tp = (

                price

                *

                (

                    1

                    +

                    TAKE_PROFIT_PERCENT

                    /

                    100

                )

            )


            sl = (

                price

                *

                (

                    1

                    -

                    STOP_LOSS_PERCENT

                    /

                    100

                )

            )





        else:


            tp = (

                price

                *

                (

                    1

                    -

                    TAKE_PROFIT_PERCENT

                    /

                    100

                )

            )


            sl = (

                price

                *

                (

                    1

                    +

                    STOP_LOSS_PERCENT

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
    # DAILY LOSS PROTECTION
    # =====================================================


    def daily_loss_check(
        self,
        loss
    ):


        max_loss = (

            self.equity

            *

            0.05

        )



        if loss >= max_loss:


            print(

                "[DAILY LOSS LIMIT]"

            )


            return False





        return True







# =====================================================
# INSTANCE
# =====================================================


risk_manager = RiskManager()
