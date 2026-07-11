# =====================================================
# order_manager.py
# VWAP SUPERTREND BOT ORDER MANAGER
# =====================================================

import time



from api.bybit_api import bybit_api



from risk.risk_manager import (

    risk_manager

)



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
    # ORDER CHECK
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


        mode = get_trading_mode()



        print(

            "[OPEN ORDER]",

            mode,

            side,

            qty

        )





        if not self.can_order():


            return None






        # Risk Check

        if not risk_manager.allow_order(

            qty

        ):


            add_log(

                "ORDER BLOCKED BY RISK"

            )


            return None








        try:



            result = bybit_api.place_order(

                side,

                qty

            )





            if not result:


                add_log(

                    "ORDER FAILED"

                )


                return None






            self.last_order_time = time.time()





            add_log(

                f"ORDER OPEN {side} {qty}"

            )





            update_status({

                "position":

                    side,


                "position_size":

                    qty

            })








            # TP / SL

            self.set_tp_sl(

                side

            )





            return result






        except Exception as e:



            add_log(

                f"ORDER ERROR {e}"

            )


            return None










    # =====================================================
    # TP SL
    # =====================================================

    def set_tp_sl(

        self,

        side

    ):


        try:



            price = bybit_api.get_price()



            if price <= 0:


                return





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






            bybit_api.set_trading_stop(

                tp,

                sl

            )



            add_log(

                f"TP SL SET {tp} {sl}"

            )



        except Exception as e:



            add_log(

                f"TP SL ERROR {e}"

            )











    # =====================================================
    # CLOSE
    # =====================================================

    def close_position(self):


        try:


            result = bybit_api.close_position()



            update_status({

                "position":

                    "NONE",


                "position_size":

                    0

            })



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
# INSTANCE
# =====================================================

order_manager = OrderManager()
