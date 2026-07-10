import time

from config import (
    DEFAULT_QTY,
    CATEGORY,
    DEFAULT_SYMBOL,
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
    # POSITION CHECK
    # ======================================

    def has_position(self):

        try:

            position = bybit_api.get_position()


            if not position:

                return False



            data = position["result"]["list"]



            for p in data:


                size = float(
                    p.get(
                        "size",
                        0
                    )
                )


                if size > 0:

                    return True



            return False



        except Exception as e:


            print(
                "[POSITION CHECK ERROR]",
                e
            )


            return False



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



            if not risk_manager.order_allowed():

                print(
                    "[ORDER BLOCK] COOLDOWN"
                )

                return None




            if self.has_position():

                print(
                    "[ORDER BLOCK] EXIST POSITION"
                )

                return None




            if not risk_manager.check_position_size(
                qty
            ):

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
    # BUY
    # ======================================

    def buy(
        self,
        qty=None
    ):


        return self.execute_order(

            "Buy",

            qty

        )




    # ======================================
    # SELL
    # ======================================

    def sell(
        self,
        qty=None
    ):


        return self.execute_order(

            "Sell",

            qty

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
