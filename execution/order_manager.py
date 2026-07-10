# execution/order_manager.py


import time
import threading



from api.bybit_api import (
    bybit_api
)


from risk.risk_manager import (
    risk_manager
)


from portfolio.position_manager import (
    position_manager
)



try:

    from database.database import (
        database
    )

except:

    database = None





class OrderManager:



    def __init__(self):


        self.lock = threading.Lock()


        self.last_order_time = 0



        print(

            "[ORDER MANAGER READY]"

        )





    # =====================================
    # EXECUTE
    # =====================================

    def execute(
        self,
        signal
    ):


        with self.lock:



            try:


                if not risk_manager.can_trade():

                    print(
                        "[ORDER BLOCK] RISK"
                    )

                    return None




                if not self.cooldown_ok():

                    print(
                        "[ORDER BLOCK] COOLDOWN"
                    )

                    return None





                if position_manager.has_position():

                    print(
                        "[ORDER BLOCK] POSITION EXISTS"
                    )

                    return None






                side = signal["side"]



                price = (

                    bybit_api.get_price()

                )



                if price is None:


                    return None






                qty = (

                    self.calculate_qty()

                )





                if not risk_manager.check_position_size(
                    qty
                ):

                    print(
                        "[ORDER BLOCK] SIZE"
                    )

                    return None






                tp, sl = (

                    self.calculate_tp_sl(

                        side,

                        price

                    )

                )







                result = (

                    self.send_order(

                        side,

                        qty,

                        tp,

                        sl

                    )

                )




                if result:


                    self.last_order_time = time.time()



                    if database:

                        database.save_order(

                            result["result"]["order"]

                        )



                return result






            except Exception as e:


                print(

                    "[EXECUTION ERROR]",

                    e

                )


                return None








    # =====================================
    # SEND ORDER RETRY
    # =====================================

    def send_order(
        self,
        side,
        qty,
        tp,
        sl
    ):


        retry = 3



        for i in range(retry):


            try:


                response = (

                    bybit_api.create_order(

                        side=side,

                        qty=qty,

                        take_profit=tp,

                        stop_loss=sl

                    )

                )



                if response:


                    print(

                        "[ORDER SUCCESS]"

                    )


                    return response





            except Exception as e:


                print(

                    "[ORDER RETRY]",

                    i,

                    e

                )



                time.sleep(1)




        return None







    # =====================================
    # TP SL
    # =====================================

    def calculate_tp_sl(
        self,
        side,
        price
    ):


        from config import (

            TAKE_PROFIT_PERCENT,

            STOP_LOSS_PERCENT

        )



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






    # =====================================
    # QTY
    # =====================================

    def calculate_qty(self):


        from config import (

            DEFAULT_QTY

        )


        return DEFAULT_QTY








    # =====================================
    # COOLDOWN
    # =====================================

    def cooldown_ok(self):


        from config import (

            ORDER_COOLDOWN

        )



        return (

            time.time()

            -

            self.last_order_time

        ) >= ORDER_COOLDOWN







    # =====================================
    # CLOSE
    # =====================================

    def close_position(self):


        try:


            position = (

                position_manager.current

            )


            if not position:

                return None





            side = position["side"]


            qty = position["size"]





            return (

                bybit_api.close_position(

                    side,

                    qty

                )

            )



        except Exception as e:


            print(

                "[CLOSE ERROR]",

                e

            )


            return None







order_manager = OrderManager()
