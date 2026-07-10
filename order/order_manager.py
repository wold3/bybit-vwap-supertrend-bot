# =====================================================
# order/order_manager.py
# =====================================================

from config import (
    DEFAULT_QTY,
    DEFAULT_SYMBOL,
)

from api.bybit_api import (
    bybit_api
)



class OrderManager:


    def __init__(self):

        print(
            "[ORDER MANAGER READY]"
        )



    # =================================================
    # EXECUTE SIGNAL
    # =================================================

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



            else:

                print(
                    "[UNKNOWN SIGNAL]",
                    signal
                )

                return False



        except Exception as e:


            print(
                "[EXECUTE ERROR]",
                e
            )

            return False



    # =================================================
    # CREATE ORDER
    # =================================================

    def create_order(
        self,
        side,
        qty=None
    ):


        try:


            if qty is None:

                qty = DEFAULT_QTY



            print(
                "[ORDER REQUEST]",
                side,
                qty
            )



            result = bybit_api.create_order(

                side,

                qty

            )



            if result is None:


                print(
                    "[ORDER FAILED]"
                )

                return False



            print(
                "[ORDER SUCCESS]",
                result
            )


            return True



        except Exception as e:


            print(
                "[CREATE ORDER ERROR]",
                e
            )


            return False



    # =================================================
    # BUY
    # =================================================

    def buy(
        self
    ):


        try:


            position = (
                bybit_api
                .get_position()
            )



            if position:


                print(
                    "[POSITION CHECK]",
                    "EXIST"
                )



            return self.create_order(

                "Buy",

                DEFAULT_QTY

            )



        except Exception as e:


            print(
                "[BUY ERROR]",
                e
            )


            return False



    # =================================================
    # SELL
    # =================================================

    def sell(
        self
    ):


        try:


            position = (
                bybit_api
                .get_position()
            )



            if position:


                print(
                    "[POSITION CHECK]",
                    "EXIST"
                )



            return self.create_order(

                "Sell",

                DEFAULT_QTY

            )



        except Exception as e:


            print(
                "[SELL ERROR]",
                e
            )


            return False



    # =================================================
    # CLOSE POSITION
    # =================================================

    def close_position(
        self
    ):


        try:


            print(
                "[CLOSE POSITION]"
            )


            result = (
                bybit_api
                .close_position()
            )


            return result



        except Exception as e:


            print(
                "[CLOSE ERROR]",
                e
            )


            return False



    # =================================================
    # STATUS
    # =================================================

    def status(
        self
    ):


        return {


            "symbol":
            DEFAULT_SYMBOL,


            "ready":
            True


        }





# Singleton

order_manager = OrderManager()
