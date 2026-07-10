# =====================================================
# execution/order_manager.py
# Bybit Order Execution Manager
# =====================================================

import time



from config import (
    DEFAULT_SYMBOL,
    DEFAULT_QTY,
    TAKE_PROFIT_PERCENT,
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


            if not signal:


                return False



            action = signal.get(

                "signal"

            )



            print(

                "[ORDER EXECUTE]",

                action

            )





            if not risk_manager.can_trade():


                print(

                    "[ORDER BLOCKED BY RISK]"

                )


                return False






            if action == "BUY":


                return self.open_position(

                    "Buy"

                )





            elif action == "SELL":


                return self.open_position(

                    "Sell"

                )





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
    # CHECK POSITION
    # =====================================================

    def has_position(self):


        try:


            position_manager.sync()



            return position_manager.has_position()



        except:


            return False







    # =====================================================
    # POSITION SIZE
    # =====================================================

    def calculate_qty(
        self,
        side
    ):


        try:


            price = (

                bybit_api

                .get_last_price()

            )



            if not price:


                return DEFAULT_QTY






            if side == "Buy":


                stop = (

                    price *

                    (

                        1 -

                        STOP_LOSS_PERCENT / 100

                    )

                )



            else:


                stop = (

                    price *

                    (

                        1 +

                        STOP_LOSS_PERCENT /100

                    )

                )






            qty = (

                risk_manager

                .calculate_position_size(

                    price,

                    stop

                )

            )





            if qty <= 0:


                qty = DEFAULT_QTY





            if not risk_manager.check_position_size(

                qty

            ):


                print(

                    "[QTY LIMIT BLOCK]"

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
    # OPEN POSITION
    # =====================================================

    def open_position(
        self,
        side
    ):


        try:



            if self.has_position():


                print(

                    "[POSITION EXISTS]"

                )


                return False






            qty = self.calculate_qty(

                side

            )



            if qty <= 0:


                return False





            print(

                "[OPEN ORDER]",

                side,

                qty

            )





            result = (

                bybit_api

                .create_order(

                    side,

                    qty

                )

            )






            if not result:


                print(

                    "[ORDER FAILED]"

                )


                return False






            print(

                "[ORDER SUCCESS]"

            )





            time.sleep(1)



            position_manager.sync()





            self.set_tp_sl()





            return True







        except Exception as e:


            print(

                "[OPEN POSITION ERROR]",

                e

            )


            return False







    # =====================================================
    # TP / SL
    # =====================================================

    def set_tp_sl(self):


        try:



            entry = (

                position_manager

                .entry_price()

            )



            side = (

                position_manager

                .side()

            )



            if entry <= 0:


                return False





            if side == "Buy":


                tp = (

                    entry *

                    (

                        1 +

                        TAKE_PROFIT_PERCENT/100

                    )

                )



                sl = (

                    entry *

                    (

                        1 -

                        STOP_LOSS_PERCENT/100

                    )

                )





            else:


                tp = (

                    entry *

                    (

                        1 -

                        TAKE_PROFIT_PERCENT/100

                    )

                )



                sl = (

                    entry *

                    (

                        1 +

                        STOP_LOSS_PERCENT/100

                    )

                )





            result = (

                bybit_api

                .set_trading_stop(

                    round(tp,2),

                    round(sl,2)

                )

            )



            if result:


                print(

                    "[TP SL SET]",

                    tp,

                    sl

                )



            return result





        except Exception as e:


            print(

                "[TP SL ERROR]",

                e

            )


            return False







    # =====================================================
    # CLOSE POSITION
    # =====================================================

    def close_position(self):


        try:


            print(

                "[CLOSE POSITION]"

            )



            result = (

                bybit_api

                .close_position()

            )



            if result:


                position_manager.clear()



            return result






        except Exception as e:


            print(

                "[CLOSE ERROR]",

                e

            )


            return False







    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "symbol":

            DEFAULT_SYMBOL,


            "position":

            position_manager.current,


            "ready":

            True


        }








# =====================================================
# SINGLETON
# =====================================================

order_manager = OrderManager()
