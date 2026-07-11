# =====================================================
# strategy/vwap_supertrend_strategy.py
# VWAP + SuperTrend Strategy
# =====================================================


from config import (
    USE_VOLUME_FILTER
)





class VWAPSuperTrendStrategy:


    def __init__(self):

        print(
            "[VWAP SUPERTREND STRATEGY READY]"
        )






    def check_signal(
        self,
        indicator
    ):


        try:


            price = indicator["price"]

            vwap = indicator["vwap"]

            trend = indicator["trend"]

            volume_ok = indicator["volume"]





            # ============================
            # Volume Filter
            # ============================

            if USE_VOLUME_FILTER:


                if not volume_ok:


                    print(
                        "[NO SIGNAL] VOLUME"
                    )


                    return None







            # ============================
            # BUY CONDITION
            # ============================


            if (


                trend == "UP"

                and

                price > vwap


            ):


                print(
                    "[SIGNAL] BUY"
                )


                return {


                    "side":

                        "Buy",


                    "reason":

                        "VWAP ABOVE + SUPERTREND UP"


                }







            # ============================
            # SELL CONDITION
            # ============================


            if (


                trend == "DOWN"

                and

                price < vwap


            ):


                print(
                    "[SIGNAL] SELL"
                )


                return {


                    "side":

                        "Sell",


                    "reason":

                        "VWAP BELOW + SUPERTREND DOWN"


                }







            print(

                "[NO SIGNAL]"

            )


            return None






        except Exception as e:


            print(

                "[STRATEGY ERROR]",

                e

            )


            return None
