import time


from api.bybit_api import bybit_api


from config import (
    DEFAULT_QTY,
    CATEGORY,
    DEFAULT_SYMBOL,
    ORDER_COOLDOWN,
)



# ==========================================
# EXECUTION ORDER MANAGER
# ==========================================

class OrderManager:


    def __init__(self):


        self.position_side = None

        self.position_qty = 0


        self.last_order_time = 0



        print("==============================")
        print("[EXECUTION ORDER MANAGER INIT]")
        print("CATEGORY :", CATEGORY)
        print("SYMBOL :", DEFAULT_SYMBOL)
        print("==============================")





    # ======================================
    # COOLDOWN CHECK
    # ======================================

    def can_order(self):


        now = time.time()



        elapsed = now - self.last_order_time



        if elapsed < ORDER_COOLDOWN:


            remain = int(

                ORDER_COOLDOWN - elapsed

            )


            print(
                "[ORDER COOLDOWN]",
                remain,
                "sec"
            )


            return False




        return True





    # ======================================
    # UPDATE POSITION
    # ======================================

    def update_position(self, position):


        try:


            side = position.get(
                "side"
            )


            size = float(

                position.get(
                    "size",
                    0
                )

            )



            if size > 0:


                self.position_side = side

                self.position_qty = size



            else:


                self.position_side = None

                self.position_qty = 0





            print(
                "[ORDER POSITION SYNC]",
                self.position_side,
                self.position_qty
            )



        except Exception as e:


            print(
                "[ORDER POSITION UPDATE ERROR]",
                e
            )





    # ======================================
    # BUY
    # ======================================

    def buy(self):


        try:



            if not self.can_order():

                return False





            if self.has_position():


                print(
                    "[BUY BLOCKED] EXIST POSITION"
                )


                return False





            print(
                "[ORDER REQUEST] BUY"
            )



            result = bybit_api.create_order(

                "Buy",

                DEFAULT_QTY

            )





            if (

                result

                and

                result.get(
                    "retCode"
                )

                ==

                0

            ):



                self.position_side = "Buy"

                self.position_qty = DEFAULT_QTY


                self.last_order_time = time.time()



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



            if not self.can_order():

                return False





            if self.has_position():


                print(
                    "[SELL BLOCKED] EXIST POSITION"
                )


                return False





            print(
                "[ORDER REQUEST] SELL"
            )




            result = bybit_api.create_order(

                "Sell",

                DEFAULT_QTY

            )





            if (

                result

                and

                result.get(
                    "retCode"
                )

                ==

                0

            ):



                self.position_side = "Sell"

                self.position_qty = DEFAULT_QTY


                self.last_order_time = time.time()



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


                side = "Sell"



            else:


                side = "Buy"





            print(
                "[CLOSE REQUEST]",
                side
            )





            result = bybit_api.create_order(

                side,

                self.position_qty

            )





            if (

                result

                and

                result.get(
                    "retCode"
                )

                ==

                0

            ):



                self.position_side = None

                self.position_qty = 0



                self.last_order_time = time.time()



                print(
                    "[POSITION CLOSED]"
                )



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
    # STATUS
    # ======================================

    def get_status(self):


        return {


            "side":

                self.position_side,


            "qty":

                self.position_qty,


            "cooldown":

                max(

                    0,

                    int(

                        ORDER_COOLDOWN -

                        (

                            time.time()

                            -

                            self.last_order_time

                        )

                    )

                )

        }





# ==========================================
# SINGLETON
# ==========================================

order_manager = OrderManager()
