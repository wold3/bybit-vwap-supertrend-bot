# =====================================================
# risk/risk_manager.py
# Risk Management System
# =====================================================

from api.bybit_api import bybit_api


from config import (

    RISK_PER_TRADE_PERCENT,

    STOP_LOSS_PERCENT,

    TAKE_PROFIT_PERCENT,

    MAX_POSITION_SIZE,

    LEVERAGE

)





class RiskManager:


    def __init__(self):


        print(

            "[RISK MANAGER READY]"

        )









    # =====================================================
    # BALANCE
    # =====================================================

    def get_balance(self):


        try:


            data = (

                bybit_api

                .get_balance()

            )



            if not data:


                return 0







            account = (

                data

                .get(

                    "result",

                    {}

                )

                .get(

                    "list",

                    []

                )

            )





            if not account:


                return 0







            coin = (

                account[0]

                .get(

                    "coin",

                    []

                )

            )





            if not coin:


                return 0





            return float(

                coin[0]

                .get(

                    "walletBalance",

                    0

                )

            )







        except Exception as e:


            print(

                "[BALANCE ERROR]",

                e

            )


            return 0










    # =====================================================
    # POSITION SIZE
    # =====================================================

    def calculate_position_size(self):


        try:


            balance = self.get_balance()





            if balance <= 0:


                # Demo 초기 오류 방어

                return MAX_POSITION_SIZE





            risk_amount = (

                balance

                *

                RISK_PER_TRADE_PERCENT

                /

                100

            )





            qty = (

                risk_amount

                *

                LEVERAGE

                /

                100000

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
    # TP / SL
    # =====================================================

    def calculate_tp_sl(

        self,

        price,

        side

    ):


        try:


            price = float(price)





            if side == "BUY":



                stop_loss = (

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



                take_profit = (

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






            else:



                stop_loss = (

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



                take_profit = (

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








            return (

                round(

                    take_profit,

                    2

                ),


                round(

                    stop_loss,

                    2

                )

            )









        except Exception as e:


            print(

                "[TP SL CALC ERROR]",

                e

            )


            return (

                0,

                0

            )









    # =====================================================
    # RISK CHECK
    # =====================================================

    def check_trade(self):


        qty = (

            self.calculate_position_size()

        )



        if qty <= 0:


            return False



        return True










# =====================================================
# INSTANCE
# =====================================================

risk_manager = RiskManager()
