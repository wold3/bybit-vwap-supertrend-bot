# execution/order_manager.py


import time
import threading



from config import (

    DEFAULT_QTY,

    ORDER_COOLDOWN,

    TAKE_PROFIT_PERCENT,

    STOP_LOSS_PERCENT,

    USE_ATR_STOP,

    ATR_STOP_MULTIPLIER,

    ATR_TP_MULTIPLIER

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



from strategy.indicators import (

    indicators

)





class OrderManager:



    def __init__(self):


        self.lock = threading.Lock()


        self.last_order_time = 0



    # =====================================
    # EXECUTE
    # =====================================

    def execute(
        self,
        signal
    ):



        with self.lock:



            try:



                if not self.cooldown_ok():

                    print(

                        "[ORDER BLOCK] COOLDOWN"

                    )

                    return None




                if not risk_manager.can_trade():


                    print(

                        "[ORDER BLOCK] RISK"

                    )

                    return None




                if position_manager.has_position():


                    print(

                        "[ORDER BLOCK] POSITION EXISTS"

                    )

                    return None




                side = signal["side"]



                qty = DEFAULT_QTY




                if not risk_manager.check_position_size(qty):


                    return None





                price = bybit_api.get_price()



                if price is None:


                    return None




                tp, sl = self.calculate_tp_sl(

                    side,

                    price

                )




                result = bybit_api.create_order(

                    side=side,

                    qty=qty,

                    take_profit=tp,

                    stop_loss=sl

                )



                if result:



                    self.last_order_time = time.time()



                    print(

                        "[ORDER SUCCESS]",

                        result

                    )



                return result




            except Exception as e:



                print(

                    "[EXECUTE ERROR]",

                    e

                )


                return None





    # =====================================
    # TP SL
    # =====================================

    def calculate_tp_sl(
        self,
        side,
        price
    ):



        if side == "Buy":



            tp = (

                price *

                (

                1 +

                TAKE_PROFIT_PERCENT / 100

                )

            )



            sl = (

                price *

                (

                1 -

                STOP_LOSS_PERCENT / 100

                )

            )




        else:



            tp = (

                price *

                (

                1 -

                TAKE_PROFIT_PERCENT / 100

                )

            )



            sl = (

                price *

                (

                1 +

                STOP_LOSS_PERCENT / 100

                )

            )




        return tp, sl





    # =====================================
    # CLOSE
    # =====================================

    def close_position(self):


        try:



            position = (

                position_manager.get()

            )



            if not position:


                print(

                    "[NO POSITION]"

                )

                return None




            return bybit_api.close_position(

                position["side"],

                position["size"]

            )



        except Exception as e:



            print(

                "[CLOSE ERROR]",

                e

            )


            return None





    # =====================================
    # COOLDOWN
    # =====================================

    def cooldown_ok(self):


        if self.last_order_time == 0:


            return True



        elapsed = (

            time.time()

            -

            self.last_order_time

        )



        return elapsed >= ORDER_COOLDOWN






    # =====================================
    # CANCEL
    # =====================================

    def cancel_all(self):


        return (

            bybit_api

            .cancel_all_orders()

        )






order_manager = OrderManager()
