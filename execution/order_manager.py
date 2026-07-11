# =====================================================
# execution/order_manager.py
# Order Execution Manager
# =====================================================

from config import (
    DEFAULT_SYMBOL
)


from api.bybit_api import (
    bybit_api
)


from risk.risk_manager import (
    risk_manager
)


from portfolio.position_manager import (
    position_manager
)


from database.database import (
    database
)


from services.telegram import (
    telegram
)


from web.server import (
    update_status,
    add_log
)





class OrderManager:


    def __init__(self):


        self.ordering = False


        print(

            "[ORDER MANAGER READY]"

        )









    # =====================================================
    # EXECUTE SIGNAL
    # =====================================================


    def execute(
        self,
        signal
    ):


        try:


            if self.ordering:


                print(

                    "[ORDER BLOCK] RUNNING"

                )

                return False






            current = (

                position_manager

                .get_position()

            )



            if current["side"] != "NONE":


                print(

                    "[ORDER BLOCK] POSITION EXISTS"

                )


                return False







            self.ordering = True







            side = signal.get(

                "side"

            )



            print(

                "[ORDER SEND]",

                side

            )






            # 현재 가격

            price = (

                signal.get(

                    "price",

                    0

                )

            )





            if price <= 0:


                print(

                    "[PRICE ERROR]"

                )


                return False







            # =========================
            # Risk Calculation
            # =========================


            risk = (

                risk_manager

                .check(

                    price

                )

            )



            if not risk:


                print(

                    "[RISK BLOCK]"

                )


                return False






            qty = risk["qty"]







            # =========================
            # SEND ORDER
            # =========================


            result = (

                bybit_api

                .place_order(

                    side,

                    qty

                )

            )







            if not result:


                return False







            if result.get(

                "retCode"

            ) != 0:


                print(

                    "[ORDER ERROR]",

                    result

                )


                return False







            print(

                "[ORDER SUCCESS]"

            )



            add_log(

                f"{side} ORDER {qty}"

            )








            update_status({

                "order":

                    side

            })







            # =========================
            # TP / SL
            # =========================


            tp_sl = (

                risk_manager

                .calculate_tp_sl(

                    side,

                    price

                )

            )





            tp_result = (

                bybit_api

                .set_trading_stop(

                    tp_sl["tp"],

                    tp_sl["sl"]

                )

            )





            print(

                "[TP SL]",

                tp_result

            )







            # =========================
            # DATABASE
            # =========================


            database.save_trade({


                "symbol":

                    DEFAULT_SYMBOL,


                "side":

                    side,


                "qty":

                    qty,


                "entry":

                    price,


                "tp":

                    tp_sl["tp"],


                "sl":

                    tp_sl["sl"],


                "result":

                    "OPEN"

            })







            # =========================
            # TELEGRAM
            # =========================


            telegram.order(

                side,

                DEFAULT_SYMBOL,

                qty,

                price

            )





            return True






        except Exception as e:


            print(

                "[ORDER MANAGER ERROR]",

                e

            )


            database.save_error(

                e

            )


            telegram.error(

                e

            )



            return False




        finally:


            self.ordering = False







# =====================================================
# INSTANCE
# =====================================================


order_manager = OrderManager()
