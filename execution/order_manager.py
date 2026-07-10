# =====================================================
# execution/order_manager.py
# Order Manager V2
# =====================================================

from config import (
    DEFAULT_SYMBOL,
    DEFAULT_QTY,
    TAKE_PROFIT_PERCENT,
    STOP_LOSS_PERCENT
)


from api.bybit_api import (
    bybit_api
)


from risk.risk_manager import (
    risk_manager
)


from portfolio.position_manager import (
    position_manager
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


        return position_manager.has_position()







    # =====================================================
    # QTY CALCULATE
    # =====================================================

    def calculate_qty(
        self,
        side
    ):


        try:



            price = (

                bybit_api

                .get_last_price()

            )



            if not price:


                return DEFAULT_QTY






            if side == "Buy":


                stop = (

                    price

                    *

                    (

                        1

                        -

                        STOP_LOSS_PERCENT/100

                    )

                )



            else:


                stop = (

                    price

                    *

                    (

                        1

                        +

                        STOP_LOSS_PERCENT/100

                    )

                )







            qty = (

                risk_manager

                .calculate_position_size(

                    price,

                    stop

                )

            )




            if qty <= 0:


                qty = DEFAULT_QTY






            qty = bybit_api.format_qty(

                qty

            )



            return qty






        except Exception as e:


            print(

                "[QTY ERROR]",

                e

            )


            return DEFAULT_QTY









    # =====================================================
    # BUY
    # =====================================================

    def buy(self):


        try:


            if self.has_position():


                print(

                    "[BUY SKIP] POSITION EXISTS"

                )


                return False






            qty = self.calculate_qty(

                "Buy"

            )



            result = bybit_api.create_order(

                "Buy",

                qty

            )



            if result:


                print(

                    "[BUY SUCCESS]"

                )


                self.set_protection(

                    "Buy"

                )


                return True




            return False





        except Exception as e:


            print(

                "[BUY ERROR]",

                e

            )


            return False









    # =====================================================
    # SELL
    # =====================================================

    def sell(self):


        try:



            if self.has_position():


                print(

                    "[SELL SKIP] POSITION EXISTS"

                )


                return False





            qty = self.calculate_qty(

                "Sell"

            )



            result = bybit_api.create_order(

                "Sell",

                qty

            )




            if result:


                print(

                    "[SELL SUCCESS]"

                )


                self.set_protection(

                    "Sell"

                )


                return True





            return False






        except Exception as e:


            print(

                "[SELL ERROR]",

                e

            )


            return False









    # =====================================================
    # TP SL
    # =====================================================

    def set_protection(
        self,
        side
    ):


        try:



            price = (

                bybit_api

                .get_last_price()

            )



            if not price:


                return False





            if side == "Buy":


                tp = (

                    price

                    *

                    (

                        1

                        +

                        TAKE_PROFIT_PERCENT/100

                    )

                )


                sl = (

                    price

                    *

                    (

                        1

                        -

                        STOP_LOSS_PERCENT/100

                    )

                )



            else:



                tp = (

                    price

                    *

                    (

                        1

                        -

                        TAKE_PROFIT_PERCENT/100

                    )

                )


                sl = (

                    price

                    *

                    (

                        1

                        +

                        STOP_LOSS_PERCENT/100

                    )

                )





            result = (

                bybit_api

                .set_trading_stop(

                    tp,

                    sl

                )

            )




            print(

                "[TP SL SET]",

                tp,

                sl

            )



            return result





        except Exception as e:


            print(

                "[TP SL ERROR]",

                e

            )


            return False









    # =====================================================
    # CLOSE
    # =====================================================

    def close_position(self):


        print(

            "[CLOSE POSITION]"

        )


        return (

            bybit_api

            .close_position()

        )









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
