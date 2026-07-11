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


    def __init__(
        self,
        bybit_api
    ):

        self.api = bybit_api


        print(
            "[ORDER MANAGER READY]"
        )





    # =====================================================
    # CREATE ORDER
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



        print(
            "[ORDER SIGNAL]",
            side
        )





        qty = DEFAULT_ORDER_QTY





        # =========================
        # TEST MODE
        # =========================

        if not LIVE:


            print(
                "[TEST ORDER]",
                side,
                qty
            )


            result = {


                "retCode":

                    0,


                "side":

                    side,


                "qty":

                    qty,


                "price":

                    price


            }





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






        # TP / SL 계산


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





        if LIVE:


            self.set_trading_stop(

                tp,

                sl

            )





        return {


            "order":

                result,


            "tp":

                tp,


            "sl":

                sl


        }









    # =====================================================
    # TP SL CALCULATION
    # =====================================================


    def calculate_tp_sl(
        self,
        side,
        entry
    ):


        if side == "Buy":


            tp = entry * (

                1 +

                TAKE_PROFIT_PERCENT / 100

            )


            sl = entry * (

                1 -

                STOP_LOSS_PERCENT / 100

            )



        else:


            tp = entry * (

                1 -

                TAKE_PROFIT_PERCENT / 100

            )


            sl = entry * (

                1 +

                STOP_LOSS_PERCENT / 100

            )



        return (

            round(tp, 2),

            round(sl, 2)

        )









    # =====================================================
    # BYBIT TP SL
    # =====================================================


    def set_trading_stop(
        self,
        tp,
        sl
    ):


        try:


            return self.api.request(

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

                        str(sl)

                }

            )


        except Exception as e:


            print(

                "[TP SL ERROR]",

                e

            )


            return None
