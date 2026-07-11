# =====================================================
# order/order_manager.py
# VWAP SUPERTREND BOT ORDER MANAGER
# BYBIT V5
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

        now = time.time()


        if now - self.last_order_time < self.cooldown:

            add_log(
                "ORDER COOLDOWN"
            )

            return False


        return True





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

                return None




            if qty is None:

                qty = MAX_POSITION_SIZE



            qty = float(qty)



            print(
                "[OPEN]",
                side,
                qty
            )





            # -----------------------------
            # RISK CHECK
            # -----------------------------

            if not risk_manager.allow_order(qty):

                add_log(
                    "ORDER BLOCKED RISK"
                )

                return None





            # -----------------------------
            # CURRENT POSITION
            # -----------------------------

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





            # -----------------------------
            # SAME POSITION
            # -----------------------------

            if current_size > 0 and current_side == side:


                add_log(
                    f"ALREADY POSITION {side}"
                )


                return None






            # -----------------------------
            # CLOSE OPPOSITE
            # -----------------------------

            if current_size > 0 and current_side != side:


                add_log(
                    "CLOSE OPPOSITE FIRST"
                )


                result = self.close_position()


                if not result:

                    return None


                time.sleep(2)







            # -----------------------------
            # LEVERAGE
            # -----------------------------

            bybit_api.set_leverage()






            # -----------------------------
            # MARKET ORDER
            # -----------------------------

            result = bybit_api.place_order(

                side=side,

                qty=qty,

                reduce_only=False

            )



            if not result:


                add_log(
                    "ORDER EMPTY RESPONSE"
                )


                return None





            if result.get(
                "retCode",
                -1
            ) != 0:


                add_log(
                    f"ORDER FAILED {result}"
                )


                return None






            self.last_order_time = time.time()





            add_log(

                f"ORDER SUCCESS {side} {qty}"

            )




            update_status({

                "position":
                    side,

                "position_size":
                    qty

            })






            # -----------------------------
            # WAIT POSITION SYNC
            # -----------------------------

            time.sleep(1)


            position_manager.refresh()



            self.set_tp_sl()



            return result





        except Exception as e:


            add_log(

                f"OPEN ORDER ERROR {e}"

            )


            return None








    # =====================================================
    # TP / SL
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




            if result:


                add_log(

                    f"TP {tp:.2f} SL {sl:.2f}"

                )


                return True




            return False




        except Exception as e:


            add_log(

                f"TP SL ERROR {e}"

            )


            return False







    # =====================================================
    # CLOSE POSITION
    # =====================================================

    def close_position(self):


        try:


            pos = position_manager.get_position()



            if pos.get(
                "size",
                0
            ) <= 0:


                add_log(
                    "NO POSITION"
                )


                return False






            result = bybit_api.close_position()



            if not result:


                add_log(
                    "CLOSE FAILED"
                )


                return False






            time.sleep(1)



            position_manager.refresh()



            self.last_order_time = time.time()



            add_log(

                "POSITION CLOSED"

            )



            return result





        except Exception as e:


            add_log(

                f"CLOSE ERROR {e}"

            )


            return False







    # =====================================================
    # EMERGENCY CLOSE
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
