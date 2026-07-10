import time


from api.bybit_api import bybit_api

from risk.risk_manager import risk_manager


from config import (
    DEFAULT_QTY,
    CATEGORY,
    DEFAULT_SYMBOL,
)



# ==========================================
# EXECUTION ORDER MANAGER
# ==========================================

class OrderManager:


    def __init__(self):


        self.position = None


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



            data = position.get(
                "result",
                {}
            ).get(
                "list",
                []
            )



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
    # BUY
    # ======================================

    def buy(
        self,
        qty=None
    ):


        return self.execute(

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


        return self.execute(

            "Sell",

            qty

        )





    # ======================================
    # EXECUTE ORDER
    # ======================================

    def execute(

        self,

        side,

        qty=None

    ):


        try:


            if not risk_manager.allow_trade():

                print(
                    "[ORDER BLOCKED] RISK"
                )

                return None




            if not risk_manager.check_cooldown():

                return None




            if qty is None:

                qty = DEFAULT_QTY




            if not risk_manager.check_position_size(

                qty

            ):


                return None




            print("==============================")
            print("[ORDER REQUEST]")
            print(
                "SIDE :",
                side
            )
            print(
                "QTY :",
                qty
            )
            print("==============================")





            response = bybit_api.create_order(

                side,

                qty

            )





            if response:


                risk_manager.register_order()



                self.position = side



                print(
                    "[ORDER SUCCESS]"
                )



                return response




            print(
                "[ORDER FAILED]"
            )


            return None




        except Exception as e:


            print(
                "[ORDER MANAGER ERROR]",
                e
            )


            return None




    # ======================================
    # CLOSE POSITION
    # ======================================

    def close_position(self):


        try:


            if self.position == "Buy":


                return self.sell()



            elif self.position == "Sell":


                return self.buy()



            return None




        except Exception as e:


            print(
                "[CLOSE ERROR]",
                e
            )


            return None





# ==========================================
# SINGLETON
# ==========================================

order_manager = OrderManager()
