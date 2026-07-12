# =====================================================
# order/order_manager.py
# VWAP SUPERTREND BOT
# BYBIT V5 ORDER MANAGER
# =====================================================


import time


from api.bybit_api import bybit_api


from risk.risk_manager import risk_manager


from portfolio.position_manager import position_manager


from config import (
    TAKE_PROFIT_PERCENT,
    STOP_LOSS_PERCENT,
    MAX_POSITION_SIZE
)


from web.server import (
    add_log,
    update_status
)





class OrderManager:



    def __init__(self):

        self.last_order_time = 0

        self.cooldown = 3


        print(
            "[ORDER MANAGER READY]"
        )





    # =====================================================
    # COOLDOWN
    # =====================================================

    def can_order(self):


        if time.time() - self.last_order_time < self.cooldown:


            add_log(
                "ORDER COOLDOWN"
            )


            return False


        return True







    # =====================================================
    # BUY LONG
    # =====================================================

    def buy(self, qty=None):


        return self.open_position(

            "Buy",

            qty

        )






    # =====================================================
    # SELL SHORT
    # =====================================================

    def sell(self, qty=None):


        return self.open_position(

            "Sell",

            qty

        )








    # =====================================================
    # OPEN POSITION
    # =====================================================

    def open_position(

        self,

        side,

        qty=None

    ):


        try:


            if not self.can_order():

                return False



            if qty is None:

                qty = MAX_POSITION_SIZE



            qty = float(qty)



            add_log(

                f"OPEN {side} {qty}"

            )





            if not risk_manager.allow_order(qty):


                add_log(

                    "RISK BLOCK"

                )


                return False







            pos = position_manager.get_position()



            current_side = pos.get(

                "side",

                "NONE"

            )



            current_size = float(

                pos.get(

                    "size",

                    0

                )

            )






            if current_size > 0 and current_side == side:


                add_log(

                    "SAME POSITION SKIP"

                )


                return False








            if current_size > 0 and current_side != side:


                add_log(

                    "CLOSE OPPOSITE"

                )


                if not self.close_position():

                    return False



                time.sleep(2)









            bybit_api.set_leverage()







            result = bybit_api.place_order(

                side,

                qty,

                False

            )







            if not result:


                add_log(

                    "ORDER FAILED"

                )


                return False







            if result.get(

                "retCode",

                -1

            ) != 0:



                add_log(

                    f"ORDER ERROR {result}"

                )


                return False







            self.last_order_time = time.time()



            add_log(

                f"ORDER SUCCESS {side}"

            )



            update_status({

                "last_action":

                f"ORDER SUCCESS {side}"

            })





            time.sleep(1)



            position_manager.refresh()



            self.set_tp_sl()



            return result







        except Exception as e:



            add_log(

                f"OPEN ERROR {e}"

            )


            return False











    # =====================================================
    # AUTO TP / SL
    # =====================================================

    def set_tp_sl(self):


        try:



            pos = position_manager.get_position()



            side = pos.get(

                "side",

                ""

            )



            entry = float(

                pos.get(

                    "entry_price",

                    0

                )

            )




            if entry <= 0:


                entry = bybit_api.get_price()



            if not entry:


                return False






            if side == "Buy":


                tp = entry * (

                    1 +

                    TAKE_PROFIT_PERCENT / 100

                )


                sl = entry * (

                    1 -

                    STOP_LOSS_PERCENT / 100

                )




            elif side == "Sell":


                tp = entry * (

                    1 -

                    TAKE_PROFIT_PERCENT / 100

                )


                sl = entry * (

                    1 +

                    STOP_LOSS_PERCENT / 100

                )



            else:


                return False







            result = bybit_api.set_trading_stop(

                round(tp,2),

                round(sl,2)

            )



            add_log(

                f"TP {tp:.2f} SL {sl:.2f}"

            )



            return result





        except Exception as e:


            add_log(

                f"TP SL ERROR {e}"

            )


            return False










    # =====================================================
    # MANUAL TP
    # =====================================================

    def set_take_profit(

        self,

        price

    ):


        try:


            return bybit_api.set_trading_stop(

                price,

                None

            )


        except Exception as e:


            add_log(

                f"TP ERROR {e}"

            )


            return False










    # =====================================================
    # MANUAL SL
    # =====================================================

    def set_stop_loss(

        self,

        price

    ):


        try:


            return bybit_api.set_trading_stop(

                None,

                price

            )


        except Exception as e:


            add_log(

                f"SL ERROR {e}"

            )


            return False










    # =====================================================
    # LEVERAGE
    # =====================================================

    def set_leverage(self):


        try:


            return bybit_api.set_leverage()



        except Exception as e:


            add_log(

                f"LEVERAGE ERROR {e}"

            )


            return False










    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):


        return self.close_position()







    def close_position(self):


        try:



            result = bybit_api.close_position()



            if result:


                position_manager.refresh()



                self.last_order_time = time.time()



                add_log(

                    "POSITION CLOSED"

                )



                update_status({

                    "last_action":

                    "POSITION CLOSED"

                })



                return True





            return False





        except Exception as e:



            add_log(

                f"CLOSE ERROR {e}"

            )


            return False











    # =====================================================
    # REVERSE
    # =====================================================

    def reverse_position(self):


        pos = position_manager.get_position()


        side = pos.get(

            "side",

            ""

        )



        size = float(

            pos.get(

                "size",

                0

            )

        )



        if size <= 0:


            return False




        self.close_position()



        time.sleep(2)



        if side == "Buy":


            return self.sell(size)



        else:


            return self.buy(size)










    # =====================================================
    # EMERGENCY
    # =====================================================

    def emergency_close(self):


        add_log(

            "EMERGENCY CLOSE"

        )


        return self.close_position()







    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "cooldown":

            self.cooldown,


            "last_order":

            self.last_order_time


        }








# =====================================================
# INSTANCE
# =====================================================

order_manager = OrderManager()
