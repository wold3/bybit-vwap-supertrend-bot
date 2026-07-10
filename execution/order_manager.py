import time
import threading


from config import (
    TP_PERCENT,
    SL_PERCENT,
)


class OrderManager:


    def __init__(
        self,
        bybit_api,
        risk_manager
    ):


        self.api = bybit_api

        self.risk = risk_manager


        self.lock = threading.Lock()


        self.last_order_time = 0


        self.cooldown = 30



    # =====================================================
    # COOLDOWN
    # =====================================================

    def cooldown_ok(self):


        now = time.time()


        if (

            now
            -
            self.last_order_time

            <
            self.cooldown

        ):

            return False



        return True



    # =====================================================
    # POSITION CHECK
    # =====================================================

    def has_position(self):


        position = self.api.get_position()


        if not position:

            return False



        try:

            size = float(

                position["result"]
                ["list"][0]
                ["size"]

            )


            return size > 0



        except:


            return False



    # =====================================================
    # TP SL CALCULATION
    # =====================================================

    def calculate_tp_sl(

        self,

        side,

        price,

        atr=None

    ):



        if atr:


            if side == "Buy":

                sl = price - (
                    atr * 2
                )

                tp = price + (
                    atr * 3
                )


            else:


                sl = price + (
                    atr * 2
                )

                tp = price - (
                    atr * 3
                )



        else:


            if side == "Buy":


                tp = price * (
                    1 + TP_PERCENT
                )

                sl = price * (
                    1 - SL_PERCENT
                )


            else:


                tp = price * (
                    1 - TP_PERCENT
                )

                sl = price * (
                    1 + SL_PERCENT
                )



        return tp, sl



    # =====================================================
    # EXECUTE ENTRY
    # =====================================================

    def execute(

        self,

        signal

    ):


        with self.lock:



            if not self.risk.can_trade():

                print(
                    "[ORDER BLOCK] RISK"
                )

                return None



            if not self.cooldown_ok():

                print(
                    "[ORDER BLOCK] COOLDOWN"
                )

                return None



            if self.has_position():

                print(
                    "[ORDER BLOCK] POSITION EXISTS"
                )

                return None



            side = signal["side"]


            price = signal["price"]


            atr = signal.get(
                "atr"
            )



            tp, sl = self.calculate_tp_sl(

                side,

                price,

                atr

            )



            qty = self.risk.calculate_position_size(

                price,

                sl

            )



            if qty <= 0:

                return None



            response = self.place_order_retry(

                side,

                qty,

                tp,

                sl

            )



            if response:


                self.last_order_time = (
                    time.time()
                )


            return response



    # =====================================================
    # RETRY ORDER
    # =====================================================

    def place_order_retry(

        self,

        side,

        qty,

        tp,

        sl,

        retry=3

    ):


        for i in range(retry):


            try:


                result = self.api.create_order(

                    side=side,

                    qty=qty,

                    take_profit=tp,

                    stop_loss=sl

                )


                if result:


                    return result



            except Exception as e:


                print(
                    "[ORDER RETRY]",
                    i,
                    e
                )



            time.sleep(2)



        return None



    # =====================================================
    # CLOSE
    # =====================================================

    def close(

        self,

        side,

        qty

    ):


        with self.lock:


            close_side = (

                "Sell"

                if side == "Buy"

                else

                "Buy"

            )


            return self.api.create_order(

                side=close_side,

                qty=qty,

                reduce_only=True

            )



order_manager = None
