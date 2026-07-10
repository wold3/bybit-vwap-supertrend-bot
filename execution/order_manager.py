import time


from config import (

    CATEGORY,

    DEFAULT_SYMBOL,

    DEFAULT_QTY,

    ORDER_COOLDOWN,

    TAKE_PROFIT_PERCENT,

    STOP_LOSS_PERCENT,

)


from api.bybit_api import bybit_api

from execution.position_manager import position_manager

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

    def cooldown_ok(self):


        now = time.time()



        if (

            now - self.last_order_time

            <

            ORDER_COOLDOWN

        ):


            print(
                "[ORDER BLOCK] COOLDOWN"
            )


            return False



        return True





    # ======================================
    # POSITION CHECK
    # ======================================

    def has_position(self):


        return position_manager.has_position()





    # ======================================
    # TP SL CALC
    # ======================================

    def calculate_tp_sl(

        self,

        side,

        price

    ):


        if side == "Buy":


            tp = (

                price

                *

                (

                    1

                    +

                    TAKE_PROFIT_PERCENT / 100

                )

            )


            sl = (

                price

                *

                (

                    1

                    -

                    STOP_LOSS_PERCENT / 100

                )

            )



        else:


            tp = (

                price

                *

                (

                    1

                    -

                    TAKE_PROFIT_PERCENT / 100

                )

            )


            sl = (

                price

                *

                (

                    1

                    +

                    STOP_LOSS_PERCENT / 100

                )

            )



        return tp, sl





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
    # EXECUTE
    # ======================================

    def execute(

        self,

        side,

        qty=None

    ):


        try:



            if qty is None:


                qty = DEFAULT_QTY





            if not self.cooldown_ok():


                return None





            if self.has_position():


                print(
                    "[ORDER BLOCK] POSITION EXISTS"
                )


                return None





            if not risk_manager.check_position_size(

                qty

            ):


                return None





            price = bybit_api.get_price()



            if price is None:


                return None





            tp, sl = self.calculate_tp_sl(


                side,


                price


            )





            print("==============================")
            print("[ORDER EXECUTE]")
            print("SIDE :", side)
            print("QTY :", qty)
            print("PRICE :", price)
            print("TP :", tp)
            print("SL :", sl)
            print("==============================")





            response = bybit_api.create_order(


                side=side,


                qty=qty,


                take_profit=tp,


                stop_loss=sl


            )





            if response and response.get("retCode") == 0:



                self.last_order_time = time.time()



                print(
                    "[ORDER SUCCESS]"
                )



                return response




            print(
                "[ORDER FAILED]"
            )



            return response





        except Exception as e:


            print(
                "[ORDER MANAGER ERROR]",
                e
            )


            return None





    # ======================================
    # CLOSE
    # ======================================

    def close_position(self):


        try:


            if not position_manager.has_position():


                return None





            side = position_manager.side


            qty = position_manager.qty





            print(
                "[CLOSE POSITION]"
            )





            return bybit_api.close_position(


                side,


                qty


            )



        except Exception as e:


            print(
                "[CLOSE ERROR]",
                e
            )


            return None





    # ======================================
    # WS POSITION UPDATE
    # ======================================

    def update_position(self, data):


        try:


            if data["side"]:


                print(
                    "[ORDER MANAGER POSITION SYNC]"
                )



            else:


                print(
                    "[ORDER MANAGER EMPTY POSITION]"
                )



        except Exception:


            pass





# ==========================================
# SINGLETON
# ==========================================

order_manager = OrderManager()
