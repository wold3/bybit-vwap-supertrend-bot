# =====================================================
# order/order_manager.py
# VWAP SUPERTREND BOT ORDER MANAGER
# =====================================================

import time


from api.bybit_api import bybit_api


from risk.risk_manager import risk_manager


from portfolio.position_manager import position_manager


from config import (

    TAKE_PROFIT_PERCENT,

    STOP_LOSS_PERCENT

)


from web.server import (

    add_log,

    update_status,

    get_trading_mode

)





class OrderManager:



    def __init__(self):


        self.last_order_time = 0


        self.cooldown = 3



        print(

            "[ORDER MANAGER READY]"

        )





    # =====================================================
    # ORDER COOLDOWN
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

        qty

    ):


        print(

            "[OPEN POSITION]",

            side,

            qty

        )


        if not self.can_order():

            return None





        # -----------------------------
        # Risk Check
        # -----------------------------

        if not risk_manager.allow_order(qty):


            add_log(

                "ORDER BLOCKED BY RISK"

            )


            return None





        try:


            current = position_manager.get_position()



            current_side = current.get(

                "side",

                "NONE"

            )



            current_size = float(

                current.get(

                    "size",

                    0

                )

            )





            # -----------------------------
            # Same Position Block
            # -----------------------------

            if current_size > 0 and current_side == side:


                add_log(

                    f"EXIST POSITION {side}"

                )


                return None





            # -----------------------------
            # Close Opposite
            # -----------------------------

            if current_size > 0 and current_side != side:


                add_log(

                    "CLOSE OPPOSITE POSITION"

                )


                close = self.close_position()



                if not close:


                    return None



                time.sleep(1)





            # -----------------------------
            # Leverage
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

                    "ORDER RESULT EMPTY"

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





            # TP SL

            self.set_tp_sl(side)



            return result





        except Exception as e:


            add_log(

                f"OPEN ORDER ERROR {e}"

            )


            return None





    # =====================================================
    # SET TP / SL
    # =====================================================

    def set_tp_sl(

        self,

        side

    ):


        try:


            price = bybit_api.get_price()



            if not price:


                return False





            if side == "Buy":


                tp = price * (

                    1 +

                    TAKE_PROFIT_PERCENT / 100

                )


                sl = price * (

                    1 -

                    STOP_LOSS_PERCENT / 100

                )



            else:


                tp = price * (

                    1 -

                    TAKE_PROFIT_PERCENT / 100

                )


                sl = price * (

                    1 +

                    STOP_LOSS_PERCENT / 100

                )





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


            result = bybit_api.close_position()



            if not result:


                add_log(

                    "CLOSE FAILED"

                )


                return None





            position_manager.reset()



            update_status({

                "position":

                    "NONE",


                "position_size":

                    0

            })



            self.last_order_time = time.time()



            add_log(

                "POSITION CLOSED"

            )



            return result





        except Exception as e:


            add_log(

                f"CLOSE ERROR {e}"

            )


            return None





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
