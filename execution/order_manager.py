# =====================================================
# execution/order_manager.py
# Order Execution Manager
# =====================================================

import time





from api.bybit_api import (

    bybit_api

)


from portfolio.position_manager import (

    position_manager

)


from risk.risk_manager import (

    risk_manager

)


from database.database import (

    database

)


from services.telegram import (

    telegram

)


from web.server import (

    add_log,

    update_status

)


from config import (

    DEFAULT_SYMBOL

)









class OrderManager:


    def __init__(self):


        self.last_order_time = 0


        self.cooldown = 30



        print(

            "[ORDER MANAGER READY]"

        )









    # =====================================================
    # EXECUTE
    # =====================================================

    def execute(

        self,

        signal

    ):


        try:



            if not signal:


                return False







            side = signal.get(

                "signal"

            )



            if side not in [


                "BUY",

                "SELL"

            ]:


                return False







            # -------------------------
            # Cooldown
            # -------------------------

            if (

                time.time()

                -

                self.last_order_time

                <

                self.cooldown

            ):


                add_log(

                    "ORDER BLOCK : COOLDOWN"

                )


                return False







            # -------------------------
            # Existing Position
            # -------------------------

            if position_manager.has_position():


                add_log(

                    "ORDER BLOCK : POSITION EXISTS"

                )


                return False







            # -------------------------
            # Risk Check
            # -------------------------

            qty = (

                risk_manager

                .calculate_position_size()

            )



            if qty <= 0:


                add_log(

                    "ORDER BLOCK : RISK"

                )


                return False







            order_side = (

                "Buy"

                if side == "BUY"

                else

                "Sell"

            )








            print(

                "[ORDER SEND]",

                order_side,

                qty

            )








            # -------------------------
            # SEND ORDER
            # -------------------------

            result = (

                bybit_api

                .place_order(

                    order_side,

                    qty

                )

            )







            if not result:


                add_log(

                    "ORDER FAILED"

                )


                return False







            if result.get(

                "retCode"

            ) != 0:


                add_log(

                    str(result)

                )


                return False







            self.last_order_time = time.time()







            add_log(

                f"ORDER SUCCESS {order_side}"

            )








            # -------------------------
            # TP / SL
            # -------------------------

            try:


                price = signal.get(

                    "price",

                    0

                )



                tp, sl = (

                    risk_manager

                    .calculate_tp_sl(

                        price,

                        side

                    )

                )



                bybit_api.set_trading_stop(

                    tp,

                    sl

                )



            except Exception as e:


                add_log(

                    f"TP SL ERROR {e}"

                )









            # -------------------------
            # DB
            # -------------------------

            database.save_trade(


                DEFAULT_SYMBOL,


                order_side,


                qty,


                signal.get(

                    "price",

                    0

                )


            )









            # -------------------------
            # Telegram
            # -------------------------

            telegram.order(


                order_side,


                DEFAULT_SYMBOL,


                qty,


                signal.get(

                    "price",

                    0

                )


            )








            update_status({


                "signal":

                    side


            })



            return True







        except Exception as e:


            print(

                "[ORDER ERROR]",

                e

            )


            database.save_error(

                e

            )


            telegram.error(

                e

            )


            return False











# =====================================================
# INSTANCE
# =====================================================

order_manager = OrderManager()
