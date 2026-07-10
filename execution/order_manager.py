# =====================================================
# execution/order_manager.py
# Order Manager
# =====================================================

import time



from config import (
    DEFAULT_SYMBOL,
    STOP_LOSS_PERCENT,
    TAKE_PROFIT_PERCENT,
    LIVE
)



from api.bybit_api import (
    bybit_api
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





            print(

                "[ORDER EXECUTE]",

                signal

            )







            # ---------------------------------
            # POSITION CHECK
            # ---------------------------------

            if position_manager.has_position():


                print(

                    "[ORDER BLOCKED]"

                    ,

                    "POSITION EXISTS"

                )


                return False







            side = signal.get(

                "side"

            )



            price = float(

                signal.get(

                    "price"

                )

            )








            qty = self.calculate_qty(

                price

            )








            result = bybit_api.create_order(

                side,

                qty

            )







            if not result:


                print(

                    "[ORDER FAILED]"

                )


                return False







            print(

                "[ORDER SUCCESS]",

                result

            )







            # ---------------------------------
            # TP / SL
            # ---------------------------------

            self.set_tp_sl(

                side,

                price

            )





            return True






        except Exception as e:



            print(

                "[ORDER MANAGER ERROR]",

                e

            )


            return False










    # =====================================================
    # QTY CALCULATION
    # =====================================================

    def calculate_qty(
        self,
        price
    ):


        try:



            # 테스트용 기본 수량


            qty = (

                0.001

            )



            return qty





        except Exception as e:


            print(

                "[QTY ERROR]",

                e

            )


            return 0










    # =====================================================
    # TP SL
    # =====================================================

    def set_tp_sl(
        self,
        side,
        entry
    ):



        try:



            if side == "Buy":



                tp = (

                    entry

                    *

                    (

                    1

                    +

                    TAKE_PROFIT_PERCENT / 100

                    )

                )



                sl = (

                    entry

                    *

                    (

                    1

                    -

                    STOP_LOSS_PERCENT / 100

                    )

                )







            else:



                tp = (

                    entry

                    *

                    (

                    1

                    -

                    TAKE_PROFIT_PERCENT / 100

                    )

                )



                sl = (

                    entry

                    *

                    (

                    1

                    +

                    STOP_LOSS_PERCENT / 100

                    )

                )







            print(

                "[TP/SL]",

                "TP:",

                tp,

                "SL:",

                sl

            )







            bybit_api.set_trading_stop(

                tp,

                sl

            )






        except Exception as e:



            print(

                "[TP SL ERROR]",

                e

            )











    # =====================================================
    # CLOSE
    # =====================================================

    def close(
        self
    ):


        print(

            "[CLOSE POSITION]"

        )



        return bybit_api.close_position()







# =====================================================
# SINGLETON
# =====================================================

order_manager = OrderManager()
