import time

from config import (
    CATEGORY,
    DEFAULT_SYMBOL,
    DEFAULT_QTY,
    ORDER_TYPE,
    TIME_IN_FORCE,
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
    # CREATE ORDER
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

            if not risk_manager.order_allowed():

                print(
                    "[ORDER BLOCK] COOLDOWN"
                )

                return None



            if not risk_manager.check_position_size(qty):

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


                risk_manager.update_order_time()



            return result



        except Exception as e:


            print(
                "[ORDER MANAGER ERROR]",
                e
            )


            return None




    # ======================================
    # LONG
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
    # SHORT
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
    # CANCEL
    # ======================================

    def cancel_all(self):

        return bybit_api.cancel_all_orders()




# ==========================================
# SINGLETON
# ==========================================

order_manager = OrderManager()
