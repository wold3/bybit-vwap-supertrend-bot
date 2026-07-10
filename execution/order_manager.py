import time
import threading


from api.bybit_api import bybit_api

from risk.risk_manager import risk_manager

from portfolio.position_manager import position_manager


from config import (
    DEFAULT_QTY,
    ATR_SL_MULTIPLIER,
    ATR_TP_MULTIPLIER
)



class OrderManager:


    def __init__(self):


        self.lock = threading.Lock()


        self.last_order_time = 0


        self.cooldown = 30



    # =====================================
    # MAIN EXECUTION
    # =====================================

    def execute(self, signal):


        with self.lock:



            if not self.validate(signal):

                return None



            side = signal["side"]



            qty = self.calculate_qty()



            if qty is None:

                return None



            atr = signal.get(
                "atr",
                0
            )



            price = signal["price"]



            tp, sl = (

                self.calculate_tp_sl(

                    side,

                    price,

                    atr

                )

            )



            order = self.place_order(

                side,

                qty,

                tp,

                sl

            )



            if order:


                self.wait_fill()


                position_manager.sync()



            return order



    # =====================================
    # VALIDATION
    # =====================================

    def validate(self, signal):


        if not risk_manager.can_trade():

            print(
                "[ORDER BLOCK RISK]"
            )

            return False



        if position_manager.has_position():

            print(
                "[POSITION EXISTS]"
            )

            return False



        if (

            time.time()

            -

            self.last_order_time

            <

            self.cooldown

        ):


            print(
                "[ORDER COOLDOWN]"
            )


            return False



        return True



    # =====================================
    # SIZE
    # =====================================

    def calculate_qty(self):


        qty = DEFAULT_QTY



        if not risk_manager.check_position_size(qty):

            return None



        return qty



    # =====================================
    # TP SL
    # =====================================

    def calculate_tp_sl(

        self,

        side,

        price,

        atr

    ):


        if atr <= 0:

            atr = price * 0.005



        if side == "Buy":


            tp = (

                price

                +

                atr *

                ATR_TP_MULTIPLIER

            )


            sl = (

                price

                -

                atr *

                ATR_SL_MULTIPLIER

            )



        else:


            tp = (

                price

                -

                atr *

                ATR_TP_MULTIPLIER

            )


            sl = (

                price

                +

                atr *

                ATR_SL_MULTIPLIER

            )



        return tp, sl



    # =====================================
    # PLACE ORDER
    # =====================================

    def place_order(

        self,

        side,

        qty,

        tp,

        sl

    ):



        for attempt in range(3):


            try:


                result = (

                    bybit_api
                    .create_order(

                        side,

                        qty,

                        tp,

                        sl

                    )

                )



                if result:


                    self.last_order_time = (

                        time.time()

                    )


                    return result



            except Exception as e:


                print(

                    "[ORDER RETRY]",

                    attempt,

                    e

                )


                time.sleep(2)



        return None



    # =====================================
    # WAIT FILL
    # =====================================

    def wait_fill(self):


        for i in range(10):


            time.sleep(1)



            pos = (

                bybit_api
                .get_position()

            )



            if pos:


                print(

                    "[FILL CONFIRMED]"

                )


                return True



        print(

            "[FILL TIMEOUT]"

        )


        return False



    # =====================================
    # CLOSE
    # =====================================

    def close_position(self):


        with self.lock:


            position = (

                position_manager
                .get()

            )


            if not position_manager.has_position():

                return False



            side = position["side"]

            qty = position["size"]



            return (

                bybit_api
                .close_position(

                    side,

                    qty

                )

            )



order_manager = OrderManager()
