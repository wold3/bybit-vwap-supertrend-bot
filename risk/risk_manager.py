# =====================================================
# risk/risk_manager.py
# Risk Management Engine
# =====================================================

import time


from config import (
    RISK_PER_TRADE_PERCENT,
    MAX_POSITION_SIZE,
    STOP_LOSS_PERCENT
)





class RiskManager:


    def __init__(self):


        self.equity = 0


        self.daily_loss = 0


        self.trade_count = 0


        self.win_count = 0


        self.loss_count = 0


        self.last_reset = time.time()



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


        self.equity = float(

            equity

        )



        print(

            "[EQUITY UPDATE]",

            self.equity

        )









    # =====================================================
    # CHECK TRADE
    # =====================================================


    def can_trade(
        self,
        current_position
    ):


        # 최대 포지션 체크

        if abs(

            float(current_position)

        ) >= MAX_POSITION_SIZE:


            print(

                "[RISK BLOCK] MAX POSITION"

            )


            return False





        # 잔고 확인

        if self.equity <= 0:


            print(

                "[RISK BLOCK] NO EQUITY"

            )


            return False





        return True







    # =====================================================
    # POSITION SIZE
    # =====================================================


    def calculate_size(
        self,
        price
    ):


        try:


            if self.equity <= 0:


                return 0





            risk_amount = (

                self.equity *

                RISK_PER_TRADE_PERCENT /

                100

            )



            stop_distance = (

                price *

                STOP_LOSS_PERCENT /

                100

            )



            qty = (

                risk_amount /

                stop_distance

            )



            if qty > MAX_POSITION_SIZE:


                qty = MAX_POSITION_SIZE





            return round(

                qty,

                3

            )



        except Exception as e:


            print(

                "[SIZE ERROR]",

                e

            )


            return 0







    # =====================================================
    # RECORD TRADE
    # =====================================================


    def record_trade(self):


        self.trade_count += 1





    # =====================================================
    # RESULT UPDATE
    # =====================================================


    def update_result(
        self,
        pnl
    ):


        pnl = float(pnl)



        if pnl >= 0:


            self.win_count += 1



        else:


            self.loss_count += 1


            self.daily_loss += abs(

                pnl

            )









    # =====================================================
    # STATISTICS
    # =====================================================


    def get_stats(self):


        winrate = 0



        if self.trade_count > 0:


            winrate = (

                self.win_count /

                self.trade_count *

                100

            )



        return {


            "trades":

                self.trade_count,


            "wins":

                self.win_count,


            "loss":

                self.loss_count,


            "winrate":

                round(

                    winrate,

                    2

                )

        }









# =====================================================
# INSTANCE
# =====================================================


risk_manager = RiskManager()
