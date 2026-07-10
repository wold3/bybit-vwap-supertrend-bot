import time

from config import (
    CATEGORY,
    DEFAULT_SYMBOL,
)

from api.bybit_api import bybit_api



# ==========================================
# POSITION MANAGER
# ==========================================


class PositionManager:



    def __init__(self):

        print("==============================")
        print("[POSITION MANAGER INIT]")
        print("CATEGORY :", CATEGORY)
        print("SYMBOL :", DEFAULT_SYMBOL)
        print("==============================")


        self.position = None




    # ======================================
    # GET CURRENT POSITION
    # ======================================

    def get_position(self):

        try:


            response = bybit_api.get_position()



            if not response:

                return None



            data = response.get(
                "result",
                {}
            )



            rows = data.get(
                "list",
                []
            )



            if len(rows) == 0:

                return None



            pos = rows[0]



            size = float(
                pos.get(
                    "size",
                    0
                )
            )



            if size == 0:

                return None



            self.position = {


                "symbol":
                    pos.get(
                        "symbol"
                    ),


                "side":
                    pos.get(
                        "side"
                    ),


                "size":
                    size,


                "entry_price":
                    float(
                        pos.get(
                            "avgPrice",
                            0
                        )
                    ),


                "unrealized_pnl":
                    float(
                        pos.get(
                            "unrealisedPnl",
                            0
                        )
                    )

            }



            return self.position




        except Exception as e:


            print(
                "[POSITION ERROR]",
                e
            )


            return None






    # ======================================
    # POSITION CHECK
    # ======================================

    def is_open(self):


        position = self.get_position()


        if position:

            return True


        return False






    # ======================================
    # CURRENT SIDE
    # ======================================

    def get_side(self):


        position = self.get_position()



        if position:

            return position["side"]



        return None






    # ======================================
    # ENTRY PRICE
    # ======================================

    def get_entry_price(self):


        position = self.get_position()



        if position:

            return position["entry_price"]



        return 0






    # ======================================
    # ATR TP / SL CALCULATION
    # ======================================

    def calculate_tp_sl(

        self,

        prices,

        multiplier=2.0

    ):


        if len(prices) < 20:

            return None, None



        high = max(
            prices[-20:]
        )


        low = min(
            prices[-20:]
        )



        atr = (
            high - low
        ) / 20



        tp = atr * multiplier


        sl = atr * multiplier



        return tp, sl







    # ======================================
    # EXIT CHECK
    # ======================================

    def check_exit(

        self,

        current_price,

        prices

    ):


        position = self.get_position()



        if not position:

            return None



        entry = position["entry_price"]


        side = position["side"]



        tp, sl = self.calculate_tp_sl(
            prices
        )



        if tp is None:

            return None





        # LONG

        if side == "Buy":


            if current_price <= entry - sl:

                return "STOP_LOSS"



            if current_price >= entry + tp:

                return "TAKE_PROFIT"





        # SHORT

        if side == "Sell":


            if current_price >= entry + sl:

                return "STOP_LOSS"



            if current_price <= entry - tp:

                return "TAKE_PROFIT"




        return None






    # ======================================
    # CLOSE POSITION
    # ======================================

    def close_position(self):


        try:


            position = self.get_position()



            if not position:

                return None



            side = position["side"]



            size = position["size"]



            close_side = (
                "Sell"
                if side == "Buy"
                else
                "Buy"
            )



            result = bybit_api.create_order(

                side=close_side,

                qty=size

            )



            print(
                "[POSITION CLOSED]"
            )


            print(result)



            return result




        except Exception as e:


            print(
                "[CLOSE ERROR]",
                e
            )


            return None






# ==========================================
# SINGLETON
# ==========================================

position_manager = PositionManager()
