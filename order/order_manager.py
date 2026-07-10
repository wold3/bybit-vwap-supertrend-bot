# =====================================================
# order/order_manager.py
# =====================================================

from config import (
    DEFAULT_QTY,
    DEFAULT_SYMBOL
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


            if not signal:

                return False



            action = (

                signal.get("signal")

                or

                signal.get("type")

                or

                signal.get("action")

            )



            if not action:


                print(

                    "[EMPTY SIGNAL]",

                    signal

                )

                return False



            action = action.upper()



            print(

                "[ORDER EXECUTE]",

                action

            )



            if action == "BUY":


                return self.buy()



            if action == "SELL":


                return self.sell()



            if action == "EXIT":


                return self.close_position()



            print(

                "[UNKNOWN ACTION]",

                action

            )


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

    def get_position(self):


        try:


            return (

                bybit_api
                .get_position()

            )


        except:


            return None




    def has_position(
        self
    ):


        try:


            data = self.get_position()



            rows = (

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



            for p in rows:


                if float(

                    p.get(

                        "size",

                        0

                    )

                    or 0

                ) > 0:


                    return True



            return False



        except:


            return False





    # =====================================================
    # QTY
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




            stop_distance = price * 0.01



            stop = (

                price - stop_distance

                if side == "Buy"

                else

                price + stop_distance

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
    # CREATE
    # =====================================================

    def create_order(
        self,
        side,
        qty
    ):


        try:


            print(

                "================"

            )

            print(

                "[ORDER REQUEST]"

            )

            print(

                "SIDE:",

                side

            )

            print(

                "QTY:",

                qty

            )



            result = (

                bybit_api
                .create_order(

                    side,

                    qty

                )

            )



            if not result:


                print(

                    "[ORDER FAILED]"

                )

                return False



            if result.get("retCode") != 0:


                print(

                    "[BYBIT ORDER ERROR]",

                    result

                )


                return False



            print(

                "[ORDER SUCCESS]"

            )


            return True



        except Exception as e:


            print(

                "[CREATE ORDER ERROR]",

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



        qty = self.calculate_qty(

            "Buy"

        )


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



        qty = self.calculate_qty(

            "Sell"

        )



        if qty <= 0:


            return False



        return self.create_order(

            "Sell",

            qty

        )





    # =====================================================
    # CLOSE
    # =====================================================

    def close_position(self):


        try:


            print(

                "[CLOSE POSITION]"

            )


            result = (

                bybit_api
                .close_position()

            )


            if result:


                print(

                    "[CLOSE SUCCESS]"

                )


            return result



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





order_manager = OrderManager()
