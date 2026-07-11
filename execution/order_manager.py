# =====================================================
# execution/order_manager.py
# Order Execution Manager
# =====================================================

from api.bybit_api import (
    bybit_api
)


from config import (
    DEFAULT_SYMBOL
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
    add_log
)





class OrderManager:


    def __init__(self):


        self.order_lock = False


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


            if self.order_lock:


                print(

                    "[ORDER BLOCK] ACTIVE ORDER"

                )


                return False







            side = signal.get(

                "side"

            )



            price = float(

                signal.get(

                    "price",

                    0

                )

            )





            if not side or price <= 0:


                return False









            # 이미 포지션 존재 확인


            if position_manager.has_position():


                print(

                    "[ORDER BLOCK] POSITION EXISTS"

                )


                return False









            # 주문 잠금


            self.order_lock = True







            # Risk 계산


            risk = (

                risk_manager

                .check(

                    price

                )

            )



            if not risk:


                self.order_lock = False


                return False







            qty = risk["qty"]





            print(

                "[ORDER SEND]",

                side,

                qty

            )









            # 주문 전송


            result = (

                bybit_api

                .place_order(

                    side,

                    qty

                )

            )





            if not result:


                self.order_lock = False


                return False







            if result.get(

                "retCode"

            ) != 0:


                print(

                    "[ORDER FAILED]",

                    result

                )


                self.order_lock = False


                return False







            print(

                "[ORDER SUCCESS]"

            )



            add_log(

                f"{side} ORDER {qty}"

            )









            # TP / SL 계산


            tp_sl = (

                risk_manager

                .calculate_tp_sl(

                    side,

                    price

                )

            )







            stop_result = (

                bybit_api

                .set_trading_stop(

                    tp_sl["tp"],

                    tp_sl["sl"]

                )

            )







            print(

                "[TP/SL]",

                tp_sl

            )









            # DB 저장


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









            # Telegram


            telegram.order(

                side,

                DEFAULT_SYMBOL,

                qty,

                price

            )



            telegram.tp_sl(

                tp_sl["tp"],

                tp_sl["sl"]

            )









            self.order_lock = False



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


            self.order_lock = False


            return False









# =====================================================
# INSTANCE
# =====================================================


order_manager = OrderManager()
