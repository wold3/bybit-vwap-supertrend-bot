# =====================================================
# risk/risk_manager.py
# Risk Manager
# =====================================================

from config import (
    RISK_PER_TRADE_PERCENT,
    MAX_POSITION_SIZE
)





class RiskManager:


    def __init__(self):


        self.equity = 0


        self.daily_loss = 0


        self.trade_count = 0


        self.max_daily_loss_percent = 3.0



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

            "[RISK EQUITY]",

            self.equity

        )








    # =====================================================
    # CHECK ENTRY
    # =====================================================


    def can_trade(
        self,
        position_size=0
    ):


        # 잔고 확인

        if self.equity <= 0:


            print(

                "[RISK BLOCK] NO EQUITY"

            )


            return False






        # 기존 포지션 확인


        if position_size > 0:


            print(

                "[RISK BLOCK] EXISTING POSITION"

            )


            return False








        # 최대 손실 확인


        max_loss = (

            self.equity *

            self.max_daily_loss_percent

            /

            100

        )



        if self.daily_loss >= max_loss:


            print(

                "[RISK BLOCK] DAILY LOSS LIMIT"

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


        risk_money = (

            self.equity *

            RISK_PER_TRADE_PERCENT

            /

            100

        )



        if price <= 0:


            return 0





        qty = (

            risk_money

            /

            price

        )



        if qty > MAX_POSITION_SIZE:


            qty = MAX_POSITION_SIZE





        return round(

            qty,

            6

        )








    # =====================================================
    # TRADE RECORD
    # =====================================================


    def record_trade(self):


        self.trade_count += 1



        print(

            "[TRADE COUNT]",

            self.trade_count

        )









    # =====================================================
    # LOSS RECORD
    # =====================================================


    def record_loss(
        self,
        amount
    ):


        self.daily_loss += abs(

            float(amount)

        )



        print(

            "[DAILY LOSS]",

            self.daily_loss

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


            "trade_count":

                self.trade_count

        }







# =====================================================
# INSTANCE
# =====================================================


risk_manager = RiskManager()
