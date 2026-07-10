from api.bybit_api import bybit_api

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


        self.position_side = None

        self.position_qty = 0


        print("==============================")
        print("[EXECUTION ORDER MANAGER INIT]")
        print("CATEGORY :", CATEGORY)
        print("SYMBOL :", DEFAULT_SYMBOL)
        print("==============================")




    # ======================================
    # UPDATE POSITION
    # ======================================

    def update_position(self, position):


        try:


            if not position:

                return



            self.position_side = position.get(
                "side"
            )


            self.position_qty = float(

                position.get(
                    "size",
                    0
                )

            )



        except Exception as e:


            print(
                "[POSITION UPDATE ERROR]",
                e
            )




    # ======================================
    # BUY
    # ======================================

    def buy(self):


        try:


            if self.has_position():

                print(
                    "[ORDER BLOCKED] EXIST POSITION"
                )

                return False




            print(
                "[ORDER REQUEST] BUY"
            )



            result = bybit_api.create_order(

                "Buy",

                DEFAULT_QTY

            )



            if result and result.get(
                "retCode"
            ) == 0:



                self.position_side = "Buy"

                self.position_qty = DEFAULT_QTY



                print(
                    "[BUY SUCCESS]"
                )


                return True




            print(
                "[BUY FAILED]",
                result
            )


            return False




        except Exception as e:


            print(
                "[BUY ERROR]",
                e
            )


            return False





    # ======================================
    # SELL
    # ======================================

    def sell(self):


        try:


            if self.has_position():

                print(
                    "[ORDER BLOCKED] EXIST POSITION"
                )

                return False




            print(
                "[ORDER REQUEST] SELL"
            )



            result = bybit_api.create_order(

                "Sell",

                DEFAULT_QTY

            )



            if result and result.get(
                "retCode"
            ) == 0:



                self.position_side = "Sell"

                self.position_qty = DEFAULT_QTY



                print(
                    "[SELL SUCCESS]"
                )


                return True




            print(
                "[SELL FAILED]",
                result
            )


            return False




        except Exception as e:


            print(
                "[SELL ERROR]",
                e
            )


            return False





    # ======================================
    # CLOSE POSITION
    # ======================================

    def close_position(self):


        try:



            if not self.has_position():

                return False





            if self.position_side == "Buy":


                close_side = "Sell"



            else:


                close_side = "Buy"





            print(
                "[CLOSE REQUEST]",
                close_side
            )



            result = bybit_api.create_order(

                close_side,

                self.position_qty

            )



            if result and result.get(
                "retCode"
            ) == 0:



                print(
                    "[POSITION CLOSED]"
                )


                self.position_side = None

                self.position_qty = 0



                return True





            print(
                "[CLOSE FAILED]",
                result
            )


            return False





        except Exception as e:


            print(
                "[CLOSE ERROR]",
                e
            )


            return False





    # ======================================
    # POSITION CHECK
    # ======================================

    def has_position(self):


        return (

            self.position_side is not None

            and

            self.position_qty > 0

        )





    # ======================================
    # GET POSITION
    # ======================================

    def get_position(self):


        return {

            "side":
                self.position_side,

            "qty":
                self.position_qty

        }





# ==========================================
# SINGLETON
# ==========================================

order_manager = OrderManager()
