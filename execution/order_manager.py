# =====================================================
# execution/order_manager.py
# Order Execution Manager
# =====================================================


from config import (
    LIVE,
    DEFAULT_SYMBOL
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


from web.server import (
    add_log,
    update_status
)





class OrderManager:



    def __init__(self):


        self.last_signal = None


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


                return





            side = signal.get(

                "side"

            )



            price = signal.get(

                "price",

                0

            )





            # -----------------------------
            # DUPLICATE FILTER
            # -----------------------------


            if side == self.last_signal:



                print(

                    "[ORDER SKIP] DUPLICATE"

                )


                return





            self.last_signal = side






            print(

                "[ORDER SIGNAL]",

                side,

                price

            )







            # -----------------------------
            # POSITION CHECK
            # -----------------------------


            position = (

                position_manager

                .get_position()

            )



            if position:


                print(

                    "[ORDER SKIP] POSITION EXISTS"

                )


                return








            # -----------------------------
            # SIZE CALCULATION
            # -----------------------------


            qty = (

                risk_manager

                .calculate_position_size(

                    price

                )

            )



            if qty <= 0:



                print(

                    "[ORDER SKIP] INVALID QTY"

                )


                return







            # -----------------------------
            # TEST / LIVE ORDER
            # -----------------------------


            result = (

                bybit_api

                .place_order(

                    side,

                    qty

                )

            )







            print(

                "[ORDER RESULT]",

                result

            )





            add_log(

                f"ORDER {side} {qty}"

            )








            update_status(

                {


                "position":

                    side


                }

            )






            return result







        except Exception as e:



            print(

                "[ORDER ERROR]",

                e

            )



            add_log(

                str(e)

            )



            return None







# =====================================================
# SINGLETON
# =====================================================

order_manager = OrderManager()
