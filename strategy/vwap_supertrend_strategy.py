# =====================================================
# strategy/vwap_supertrend_strategy.py
# VWAP + SuperTrend Strategy
# =====================================================

from config import (
    USE_VOLUME_FILTER,
    MIN_VOLUME_MULTIPLIER
)


from indicators.indicator_engine import (
    indicator_engine
)





class VWAPSuperTrendStrategy:



    def __init__(self):


        self.last_indicator = {


            "vwap":0,


            "trend":"NONE",


            "volume":False


        }


        print(

            "[VWAP SUPERTREND STRATEGY READY]"

        )









    # =====================================================
    # ANALYZE
    # =====================================================

    def analyze(
        self,
        candles
    ):


        try:



            if len(candles) < 50:


                return None





            result = (

                indicator_engine.calculate(

                    candles

                )

            )





            price = float(

                candles[-1]

                ["close"]

            )





            vwap = result.get(

                "vwap",

                0

            )





            trend = result.get(

                "trend",

                "NONE"

            )





            volume_ok = result.get(

                "volume",

                False

            )








            self.last_indicator = {


                "vwap":

                    vwap,


                "trend":

                    trend,


                "volume":

                    volume_ok


            }







            print(

                "[INDICATOR]",

                "PRICE:",

                price,

                "VWAP:",

                round(vwap,2),

                "TREND:",

                trend,

                "VOLUME:",

                volume_ok

            )









            # -----------------------------
            # VOLUME FILTER
            # -----------------------------


            if USE_VOLUME_FILTER:


                if not volume_ok:


                    print(

                        "[NO SIGNAL] VOLUME"

                    )


                    return None







            # -----------------------------
            # BUY
            # -----------------------------


            if (


                trend == "UP"


                and


                price > vwap


            ):



                return {


                    "signal":

                        "BUY",


                    "side":

                        "Buy",


                    "price":

                        price


                }









            # -----------------------------
            # SELL
            # -----------------------------


            if (


                trend == "DOWN"


                and


                price < vwap


            ):



                return {


                    "signal":

                        "SELL",


                    "side":

                        "Sell",


                    "price":

                        price


                }







            return None






        except Exception as e:



            print(

                "[STRATEGY ERROR]",

                e

            )


            return None







# =====================================================
# SINGLETON
# =====================================================

vwap_supertrend_strategy = VWAPSuperTrendStrategy()
