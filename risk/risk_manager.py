# =====================================================
# risk/risk_manager.py
# Risk Management
# =====================================================

from config import (
    RISK_PER_TRADE_PERCENT,
    LEVERAGE,
    MAX_POSITION_SIZE
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


        self.equity = float(

            equity

        )


        print(

            "[RISK READY]",

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






            # 위험 금액

            risk_amount = (

                self.equity

                *

                RISK_PER_TRADE_PERCENT

                /

                100

            )





            # 레버리지 적용

            position_value = (

                risk_amount

                *

                LEVERAGE

            )






            qty = (

                position_value

                /

                float(price)

            )






            # 최대 제한


            if qty > MAX_POSITION_SIZE:


                qty = MAX_POSITION_SIZE






            # Bybit 최소 단위 보정

            qty = round(

                qty,

                3

            )





            return qty





        except Exception as e:



            print(

                "[RISK ERROR]",

                e

            )


            return 0







    # =====================================================
    # RISK CHECK
    # =====================================================

    def check_risk(self):


        if self.equity <= 0:


            return False



        return True







# =====================================================
# SINGLETON
# =====================================================

risk_manager = RiskManager()
