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

from risk.risk_manager import (
    risk_manager
)



class OrderManager:


    def __init__(self):

        print(
            "[ORDER MANAGER READY]"
        )



    # =====================================================
    # EXECUTE SIGNAL
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



    # =====================================================
    # POSITION CHECK
    # =====================================================

    def has_position(
        self,
        position
    ):

        try:

            if position is None:

                return False



            rows = (
                position
                .get("result", {})
                .get("list", [])
            )



            for p in rows:


                size = float(

                    p.get(
                        "size",
                        0
                    )

                )


                if size > 0:

                    return True



            return False



        except Exception:

            return False



    # =====================================================
    # CREATE ORDER
    # =====================================================

    def create_order(
        self,
        side,
        qty
    ):


        try:


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



            if result is None:


                print(
                    "[ORDER FAILED]"
                )

                return False



            print(
                "[ORDER SUCCESS]"
            )


            return True



        except Exception as e:


            print(
                "[ORDER ERROR]",
                e
            )

            return False



    # =====================================================
    # CALCULATE QTY
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


            if price is None:

                return DEFAULT_QTY



            if side == "Buy":

                stop = price * 0.99


            else:

                stop = price * 1.01



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
                    "[POSITION SIZE BLOCK]"
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
    # BUY
    # =====================================================

    def buy(
        self
    ):


        try:


            position = (
                bybit_api
                .get_position()
            )



            if self.has_position(
                position
            ):


                print(
                    "[POSITION EXISTS]"
                )


                print(
                    "[BUY SKIPPED]"
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



        except Exception as e:


            print(
                "[BUY ERROR]",
                e
            )


            return False



    # =====================================================
    # SELL
    # =====================================================

    def sell(
        self
    ):


        try:


            position = (
                bybit_api
                .get_position()
            )



            if self.has_position(
                position
            ):


                print(
                    "[POSITION EXISTS]"
                )


                print(
                    "[SELL SKIPPED]"
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



        except Exception as e:


            print(
                "[SELL ERROR]",
                e
            )


            return False



    # =====================================================
    # CLOSE POSITION
    # =====================================================

    def close_position(
        self
    ):


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

    def status(
        self
    ):


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
