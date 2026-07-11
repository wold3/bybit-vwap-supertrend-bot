# =====================================================
# execution/order_manager.py
# Order Manager + Risk Guard
# =====================================================

from config import (
    LIVE_ORDER,
    DEFAULT_ORDER_QTY,
    STOP_LOSS_PERCENT,
    TAKE_PROFIT_PERCENT
)


from risk.risk_manager import (
    risk_manager
)


from portfolio.position_manager import (
    position_manager
)





class OrderManager:


    def __init__(self, api):

        self.api = api


        print(
            "[ORDER MANAGER READY]"
        )







    # =====================================================
    # EXECUTE ORDER
    # =====================================================


    def execute(
        self,
        signal,
        price
    ):


        if not signal:


            return None





        side = signal.get(

            "side"

        )



        if side not in [

            "Buy",

            "Sell"

        ]:


            print(

                "[INVALID SIGNAL]",

                signal

            )


            return None







        # =============================
        # RISK CHECK
        # =============================


        position = (

            position_manager

            .get_position()

        )



        if not risk_manager.can_trade(

            position.get(

                "size",

                0

            )

        ):


            print(

                "[ORDER BLOCKED BY RISK]"

            )


            return None





        print(

            "[RISK OK]"

        )








        # =============================
        # ORDER SIZE
        # =============================


        qty = DEFAULT_ORDER_QTY



        calculated = (

            risk_manager

            .calculate_size(

                price

            )

        )



        if calculated > 0:


            qty = calculated







        print(

            "[ORDER SEND]",

            side,

            qty

        )







        # =============================
        # TEST MODE
        # =============================


        if not LIVE_ORDER:


            result = {


                "retCode":

                    0,


                "retMsg":

                    "LOCAL TEST ORDER",


                "side":

                    side,


                "qty":

                    qty


            }







        # =============================
        # BYBIT ORDER
        # =============================


        else:



            result = self.api.place_order(

                side,

                qty

            )





        if not result:


            print(

                "[ORDER FAILED]"

            )


            return None







        if result.get(

            "retCode",

            0

        ) != 0:


            print(

                "[BYBIT ORDER ERROR]",

                result

            )


            return None







        print(

            "[ORDER SUCCESS]",

            result

        )



        risk_manager.record_trade()







        # =============================
        # TP / SL
        # =============================


        tp, sl = self.calculate_tp_sl(

            side,

            price

        )




        if LIVE_ORDER:


            self.api.set_trading_stop(

                tp,

                sl

            )




        return {


            "side":

                side,


            "qty":

                qty,


            "entry":

                price,


            "tp":

                tp,


            "sl":

                sl,


            "response":

                result

        }









    # =====================================================
    # TP SL CALCULATE
    # =====================================================


    def calculate_tp_sl(
        self,
        side,
        price
    ):


        if side == "Buy":


            tp = price * (

                1 +

                TAKE_PROFIT_PERCENT / 100

            )


            sl = price * (

                1 -

                STOP_LOSS_PERCENT / 100

            )


        else:


            tp = price * (

                1 -

                TAKE_PROFIT_PERCENT / 100

            )


            sl = price * (

                1 +

                STOP_LOSS_PERCENT / 100

            )




        return (

            round(tp,2),

            round(sl,2)

        )








# =====================================================
# INSTANCE
# =====================================================


from api.bybit_api import bybit_api


order_manager = OrderManager(

    bybit_api

)
