# =====================================================
# execution/order_manager.py
# Order Manager
# =====================================================

from config import (
    LIVE,
    DEFAULT_ORDER_QTY,
    CATEGORY,
    DEFAULT_SYMBOL,
    STOP_LOSS_PERCENT,
    TAKE_PROFIT_PERCENT
)





class OrderManager:


    def __init__(self, api):

        self.api = api


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
            "side"
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






        qty = DEFAULT_ORDER_QTY





        print(

            "[ORDER SIGNAL]",

            side

        )








        # =================================================
        # TEST MODE
        # =================================================


        if not LIVE:


            print(

                "[TEST ORDER]",

                side,

                qty

            )



            order_result = {


                "retCode":

                    0,


                "retMsg":

                    "TEST ORDER",


                "side":

                    side,


                "qty":

                    qty,


                "price":

                    price


            }







        # =================================================
        # LIVE MODE
        # =================================================


        else:


            order_result = self.api.place_order(

                side,

                qty

            )







            if not order_result:


                print(

                    "[ORDER FAILED]"

                )


                return None







        tp, sl = self.calculate_tp_sl(

            side,

            price

        )




        print(

            "[TP]",

            tp

        )


        print(

            "[SL]",

            sl

        )






        # LIVE에서만 등록

        if LIVE:


            self.set_tp_sl(

                tp,

                sl

            )






        return {


            "order":

                order_result,


            "side":

                side,


            "entry":

                price,


            "take_profit":

                tp,


            "stop_loss":

                sl


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
    # SET TP SL
    # =====================================================


    def set_tp_sl(
        self,
        tp,
        sl
    ):


        try:


            result = self.api.request(

                "POST",

                "/v5/position/trading-stop",

                {


                    "category":

                        CATEGORY,


                    "symbol":

                        DEFAULT_SYMBOL,


                    "takeProfit":

                        str(tp),


                    "stopLoss":

                        str(sl),


                    "tpslMode":

                        "Full"

                }

            )



            print(

                "[TP SL SET]",

                result

            )



            return result





        except Exception as e:


            print(

                "[TP SL ERROR]",

                e

            )


            return None







# =====================================================
# SINGLETON
# =====================================================

from api.bybit_api import bybit_api


order_manager = OrderManager(

    bybit_api

)
