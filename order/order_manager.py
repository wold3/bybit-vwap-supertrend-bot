# =====================================================
# order/order_manager.py
# Order Manager
# =====================================================

from config import (
    DEFAULT_QTY,
    DEFAULT_SYMBOL,
    STOP_LOSS_PERCENT,
    TAKE_PROFIT_PERCENT
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







class OrderManager:



    def __init__(self):


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



            action = signal.get(

                "signal"

            )



            print(

                "[ORDER EXECUTE]",

                action

            )



            if action == "BUY":


                return self.buy()



            elif action == "SELL":


                return self.sell()



            elif action == "EXIT":


                return self.close_position()



            return False



        except Exception as e:


            print(

                "[EXECUTE ERROR]",

                e

            )


            return False







    # =====================================================
    # POSITION CHECK
    # =====================================================

    def has_position(self):


        try:


            position = bybit_api.get_position()



            rows = (

                position

                .get("result", {})

                .get("list", [])

            )



            for p in rows:


                if float(

                    p.get(

                        "size",

                        0

                    )

                ) > 0:


                    return True



            return False



        except:


            return False







    # =====================================================
    # QTY
    # =====================================================

    def calculate_qty(self):


        try:


            if not risk_manager.can_trade():


                return 0



            price = bybit_api.get_last_price()



            if price is None:


                return DEFAULT_QTY



            qty = risk_manager.calculate_position_size(

                price,

                price * 0.99

            )



            if qty <= 0:


                qty = DEFAULT_QTY



            if not risk_manager.check_position_size(qty):


                print(

                    "[POSITION SIZE BLOCK]"

                )


                return 0



            return round(

                qty,

                3

            )



        except Exception as e:


            print(

                "[QTY ERROR]",

                e

            )


            return DEFAULT_QTY







    # =====================================================
    # TP SL CALCULATION
    # =====================================================

    def calculate_tp_sl(
        self,
        side,
        price
    ):


        if side == "Buy":


            stop = (

                price

                *

                (

                    1 -

                    STOP_LOSS_PERCENT / 100

                )

            )


            tp = (

                price

                *

                (

                    1 +

                    TAKE_PROFIT_PERCENT / 100

                )

            )



        else:


            stop = (

                price

                *

                (

                    1 +

                    STOP_LOSS_PERCENT / 100

                )

            )


            tp = (

                price

                *

                (

                    1 -

                    TAKE_PROFIT_PERCENT / 100

                )

            )



        return tp, stop







    # =====================================================
    # BUY
    # =====================================================

    def buy(self):


        if self.has_position():


            print(

                "[BUY SKIP] POSITION EXISTS"

            )


            return False



        qty = self.calculate_qty()



        if qty <= 0:


            return False



        result = bybit_api.create_order(

            "Buy",

            qty

        )



        if result:


            price = bybit_api.get_last_price()



            if price:


                tp, sl = self.calculate_tp_sl(

                    "Buy",

                    price

                )


                bybit_api.set_trading_stop(

                    tp,

                    sl

                )



            database.save_order(

                "Buy",

                qty,

                result

            )



            print(

                "[BUY COMPLETE]"

            )


            return True



        return False







    # =====================================================
    # SELL
    # =====================================================

    def sell(self):


        if self.has_position():


            print(

                "[SELL SKIP] POSITION EXISTS"

            )


            return False



        qty = self.calculate_qty()



        if qty <= 0:


            return False



        result = bybit_api.create_order(

            "Sell",

            qty

        )



        if result:


            price = bybit_api.get_last_price()



            if price:


                tp, sl = self.calculate_tp_sl(

                    "Sell",

                    price

                )


                bybit_api.set_trading_stop(

                    tp,

                    sl

                )



            database.save_order(

                "Sell",

                qty,

                result

            )



            print(

                "[SELL COMPLETE]"

            )


            return True



        return False







    # =====================================================
    # CLOSE
    # =====================================================

    def close_position(self):


        print(

            "[CLOSE POSITION]"

        )


        return bybit_api.close_position()







    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "symbol":

                DEFAULT_SYMBOL,


            "ready":

                True


        }







# =====================================================
# SINGLETON
# =====================================================

order_manager = OrderManager()
