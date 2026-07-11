# =====================================================
# execution/order_manager.py
# Order Manager
# =====================================================

import time


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


        self.last_order = {}



        print(
            "[ORDER MANAGER READY]"
        )







    # =====================================================
    # EXECUTE
    # =====================================================


    def execute(
        self,
        signal,
        price
    ):


        if not signal:


            return None





        side = signal.get(

            "side",

            ""

        )



        if side not in [

            "Buy",

            "Sell"

        ]:


            print(

                "[INVALID SIDE]",

                side

            )


            return None







        # =================================================
        # POSITION CHECK
        # =================================================


        position = (

            position_manager

            .get_position()

        )



        current_size = float(

            position.get(

                "size",

                0

            )

        )



        if not risk_manager.can_trade(

            current_size

        ):


            print(

                "[ORDER BLOCKED]"

            )


            return None





        print(

            "[RISK OK]"

        )







        # =================================================
        # SIZE
        # =================================================


        qty = DEFAULT_ORDER_QTY



        calculated_qty = (

            risk_manager

            .calculate_size(

                price

            )

        )



        if calculated_qty > 0:


            qty = calculated_qty








        print(

            "[ORDER SEND]",

            side,

            qty

        )








        # =================================================
        # ORDER
        # =================================================


        if LIVE_ORDER:


            result = (

                self.api

                .place_order(

                    side,

                    qty

                )

            )


        else:


            result = {


                "retCode":

                    0,


                "retMsg":

                    "LOCAL TEST ORDER",


                "result":

                    {

                        "orderId":

                            "TEST_ORDER"

                    }

            }








        if not result:


            print(

                "[ORDER FAILED]"

            )


            return None







        if result.get(

            "retCode"

        ) != 0:



            print(

                "[BYBIT ORDER ERROR]",

                result

            )


            return None







        order_id = (

            result

            .get(

                "result",

                {}

            )

            .get(

                "orderId",

                ""

            )

        )







        self.last_order = {


            "order_id":

                order_id,


            "side":

                side,


            "qty":

                qty,


            "price":

                price,


            "time":

                time.time()

        }






        print(

            "[ORDER SUCCESS]",

            self.last_order

        )






        risk_manager.record_trade()







        # =================================================
        # TP SL
        # =================================================


        tp, sl = (

            self.calculate_tp_sl(

                side,

                price

            )

        )




        if LIVE_ORDER:


            tpsl_result = (

                self.api

                .set_trading_stop(

                    tp,

                    sl

                )

            )


            print(

                "[TP SL RESULT]",

                tpsl_result

            )



        else:


            print(

                "[LOCAL TP SL]",

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


            "order_id":

                order_id,


            "response":

                result

        }









    # =====================================================
    # TP SL CALCULATOR
    # =====================================================


    def calculate_tp_sl(
        self,
        side,
        price
    ):


        if side == "Buy":


            tp = (

                price *

                (

                    1 +

                    TAKE_PROFIT_PERCENT / 100

                )

            )


            sl = (

                price *

                (

                    1 -

                    STOP_LOSS_PERCENT / 100

                )

            )



        else:


            tp = (

                price *

                (

                    1 -

                    TAKE_PROFIT_PERCENT / 100

                )

            )


            sl = (

                price *

                (

                    1 +

                    STOP_LOSS_PERCENT / 100

                )

            )





        return (

            round(tp, 2),

            round(sl, 2)

        )









    # =====================================================
    # LAST ORDER
    # =====================================================


    def get_last_order(self):


        return self.last_order







# =====================================================
# INSTANCE
# =====================================================


from api.bybit_api import bybit_api



order_manager = OrderManager(

    bybit_api

)
