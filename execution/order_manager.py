import time

from config import (
    CATEGORY,
    DEFAULT_SYMBOL,
    DEFAULT_QTY,
    ORDER_COOLDOWN,
)

from api.bybit_api import bybit_api
from risk.risk_manager import risk_manager



# ==========================================
# ORDER MANAGER
# ==========================================


class OrderManager:



    def __init__(self):

        self.last_order_time = 0


        print("==============================")
        print("[EXECUTION ORDER MANAGER INIT]")
        print("CATEGORY :", CATEGORY)
        print("SYMBOL :", DEFAULT_SYMBOL)
        print("==============================")





    # ======================================
    # COOLDOWN CHECK
    # ======================================

    def cooldown_check(self):


        elapsed = (
            time.time()
            -
            self.last_order_time
        )


        if elapsed < ORDER_COOLDOWN:

            print(
                "[ORDER BLOCK]"
            )

            print(
                "COOLDOWN:",
                round(
                    ORDER_COOLDOWN - elapsed,
                    1
                ),
                "sec"
            )

            return False



        return True






    # ======================================
    # EXECUTE ORDER
    # ======================================

    def execute_order(

        self,

        side,

        qty=None

    ):


        try:


            if qty is None:

                qty = DEFAULT_QTY





            # risk check

            if not self.cooldown_check():

                return None




            if not risk_manager.order_allowed():

                print(
                    "[RISK BLOCK]"
                )

                return None





            if not risk_manager.check_position_size(qty):

                print(
                    "[SIZE BLOCK]"
                )

                return None






            print("==============================")
            print("[ORDER REQUEST]")
            print("SIDE :", side)
            print("QTY :", qty)
            print("==============================")





            result = bybit_api.create_order(

                side=side,

                qty=qty

            )






            if result:


                self.last_order_time = time.time()


                risk_manager.update_order_time()



                print(
                    "[ORDER SUCCESS]"
                )



            return result





        except Exception as e:


            print(
                "[ORDER MANAGER ERROR]",
                e
            )


            return None






    # ======================================
    # LONG ENTRY
    # ======================================

    def buy(

        self,

        qty=None

    ):


        return self.execute_order(

            side="Buy",

            qty=qty

        )







    # ======================================
    # SHORT ENTRY
    # ======================================

    def sell(

        self,

        qty=None

    ):


        return self.execute_order(

            side="Sell",

            qty=qty

        )







    # ======================================
    # CANCEL ALL ORDERS
    # ======================================

    def cancel_all(self):


        try:


            return bybit_api.cancel_all_orders()



        except Exception as e:


            print(
                "[CANCEL ERROR]",
                e
            )


            return None







# ==========================================
# SINGLETON
# ==========================================

order_manager = OrderManager()
