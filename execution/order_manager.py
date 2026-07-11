# =====================================================
# execution/order_manager.py
# Order Manager
# =====================================================

from config import (
    DEFAULT_SYMBOL,
    STOP_LOSS_PERCENT
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


            side = signal.get(

                "side"

            )



            if side not in [

                "Buy",

                "Sell"

            ]:


                return False






            current = (

                position_manager

                .get_position()

                .get(

                    "size",

                    0

                )

            )





            if not risk_manager.can_trade(

                current

            ):


                add_log(

                    "RISK BLOCK"

                )


                return False









            price = (

                self.get_price()

            )



            if price <= 0:


                return False






            qty = (

                risk_manager

                .calculate_size(

                    price

                )

            )



            if qty <= 0:


                return False







            print(

                "[ORDER SEND]",

                side,

                qty

            )







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

                    "[ORDER FAILED]",

                    result

                )



                return False








            print(

                "[ORDER SUCCESS]"

            )





            risk_manager.record_trade()









            # =========================
            # TP / SL 계산
            # =========================


            if side == "Buy":


                tp = (

                    price *

                    1.02

                )


                sl = (

                    price *

                    (

                    1 -

                    STOP_LOSS_PERCENT

                    /

                    100

                    )

                )



            else:


                tp = (

                    price *

                    0.98

                )


                sl = (

                    price *

                    (

                    1 +

                    STOP_LOSS_PERCENT

                    /

                    100

                    )

                )









            tp_result = (

                bybit_api

                .set_trading_stop(

                    round(tp,2),

                    round(sl,2)

                )

            )





            print(

                "[TP SL RESULT]",

                tp_result

            )









            trade = {


                "symbol":

                    DEFAULT_SYMBOL,


                "side":

                    side,


                "qty":

                    qty,


                "entry":

                    price,


                "tp":

                    tp,


                "sl":

                    sl,


                "result":

                    "OPEN"

            }





            database.save_trade(

                trade

            )









            update_status({


                "order":

                    side,


                "tp":

                    tp,


                "sl":

                    sl

            })





            add_log(

                str(trade)

            )









            telegram.send(

f"""
🚀 VWAP SUPERTREND BOT

SIDE : {side}

SYMBOL : {DEFAULT_SYMBOL}

ENTRY : {price}

QTY : {qty}

TP : {round(tp,2)}

SL : {round(sl,2)}

MODE : AUTO
"""

            )







            return True







        except Exception as e:


            print(

                "[ORDER ERROR]",

                e

            )


            database.save_error(

                e

            )


            return False










    # =====================================================
    # CURRENT PRICE
    # =====================================================


    def get_price(self):


        try:


            from api.bybit_api import (

                bybit_api

            )



            data = (

                bybit_api

                .get_kline()

            )



            if data:


                return float(

                    data[-1][4]

                )



        except:


            pass




        return 0









# =====================================================
# INSTANCE
# =====================================================


order_manager = OrderManager()
