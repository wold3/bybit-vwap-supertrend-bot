# =====================================================
# order/order_manager.py
# Bybit V5 Unified Order Manager
# =====================================================


from config import (
    DEFAULT_QTY,
    DEFAULT_SYMBOL,
    STOP_LOSS_PERCENT,
    TAKE_PROFIT_PERCENT,
)


from api.bybit_api import (
    bybit_api
)


from risk.risk_manager import (
    risk_manager
)





class OrderManager:



    def __init__(self):

        print(
            "[ORDER MANAGER READY]"
        )







    # =====================================================
    # EXECUTE
    # =====================================================

    def execute(
        self,
        signal
    ):


        try:


            if signal is None:

                return False




            action = signal.get(
                "signal"
            )



            print(
                "[ORDER EXECUTE]",
                action
            )




            if action == "BUY":


                return self.buy()



            elif action == "SELL":


                return self.sell()



            elif action == "EXIT":


                return self.close_position()



            return False




        except Exception as e:


            print(
                "[EXECUTE ERROR]",
                e
            )


            return False







    # =====================================================
    # POSITION CHECK
    # =====================================================

    def has_position(self):


        try:


            position = (
                bybit_api
                .get_position()
            )



            rows = (

                position
                .get(
                    "result",
                    {}
                )
                .get(
                    "list",
                    []
                )

            )



            for p in rows:


                if float(

                    p.get(
                        "size",
                        0
                    )

                ) > 0:


                    return True





            return False



        except Exception:


            return False







    # =====================================================
    # QTY
    # =====================================================

    def calculate_qty(self):


        try:


            price = (
                bybit_api
                .get_last_price()
            )


            if price is None:

                return DEFAULT_QTY





            stop_distance = (

                price

                *

                STOP_LOSS_PERCENT

                /

                100

            )



            stop_price = (

                price

                -

                stop_distance

            )



            qty = (

                risk_manager
                .calculate_position_size(

                    price,

                    stop_price

                )

            )



            if qty <= 0:


                qty = DEFAULT_QTY




            if not risk_manager.check_position_size(qty):


                print(
                    "[QTY BLOCK]"
                )


                return 0




            return round(

                qty,

                3

            )




        except Exception as e:


            print(
                "[QTY ERROR]",
                e
            )


            return DEFAULT_QTY







    # =====================================================
    # CREATE ORDER
    # =====================================================

    def create_order(
        self,
        side,
        qty
    ):



        try:



            price = (
                bybit_api
                .get_last_price()
            )



            if price is None:

                return False





            if side == "Buy":


                stop_loss = (

                    price

                    *

                    (

                        1

                        -

                        STOP_LOSS_PERCENT / 100

                    )

                )


                take_profit = (

                    price

                    *

                    (

                        1

                        +

                        TAKE_PROFIT_PERCENT / 100

                    )

                )




            else:


                stop_loss = (

                    price

                    *

                    (

                        1

                        +

                        STOP_LOSS_PERCENT / 100

                    )

                )



                take_profit = (

                    price

                    *

                    (

                        1

                        -

                        TAKE_PROFIT_PERCENT / 100

                    )

                )







            print(
                "[ORDER REQUEST]",
                side,
                qty
            )




            result = (

                bybit_api
                .session
                .place_order(

                    category="linear",

                    symbol=DEFAULT_SYMBOL,

                    side=side,

                    orderType="Market",

                    qty=str(qty),


                    stopLoss=str(
                        round(
                            stop_loss,
                            2
                        )
                    ),


                    takeProfit=str(
                        round(
                            take_profit,
                            2
                        )
                    )

                )

            )



            if result.get(
                "retCode"
            ) == 0:



                print(
                    "[ORDER SUCCESS]",
                    result
                )

                return True





            print(
                "[ORDER FAILED]",
                result
            )



            return False




        except Exception as e:


            print(
                "[ORDER ERROR]",
                e
            )


            return False







    # =====================================================
    # BUY
    # =====================================================

    def buy(self):


        if self.has_position():


            print(
                "[BUY SKIP POSITION EXISTS]"
            )


            return False





        qty = self.calculate_qty()



        if qty <= 0:

            return False





        return self.create_order(

            "Buy",

            qty

        )








    # =====================================================
    # SELL
    # =====================================================

    def sell(self):


        if self.has_position():


            print(
                "[SELL SKIP POSITION EXISTS]"
            )


            return False





        qty = self.calculate_qty()



        if qty <= 0:

            return False





        return self.create_order(

            "Sell",

            qty

        )








    # =====================================================
    # CLOSE POSITION
    # =====================================================

    def close_position(self):


        try:


            print(
                "[CLOSE POSITION]"
            )



            return (

                bybit_api
                .close_position()

            )



        except Exception as e:


            print(
                "[CLOSE ERROR]",
                e
            )


            return False







    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "symbol":

                DEFAULT_SYMBOL,


            "ready":

                True


        }








# =====================================================
# SINGLETON
# =====================================================

order_manager = OrderManager()
