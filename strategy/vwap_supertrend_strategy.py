# strategy/vwap_supertrend_strategy.py

import pandas as pd

from config import (
    VWAP_LENGTH,
    ST_LENGTH,
    SUPERTREND_PERIOD,
    SUPERTREND_MULTIPLIER,

    USE_VOLUME_FILTER,
    MIN_VOLUME_MULTIPLIER
)


from indicators.indicators import (
    Indicators
)



class VWAPSupertrendStrategy:


    def __init__(self):

        self.indicators = Indicators()



    # =====================================
    # ANALYZE
    # =====================================

    def analyze(
        self,
        candles
    ):


        try:


            if candles is None:

                return None



            if len(candles) < 50:

                return None



            df = pd.DataFrame(
                candles
            )



            # =============================
            # DATA
            # =============================

            opens = (
                df["open"]
                .astype(float)
                .tolist()
            )


            highs = (
                df["high"]
                .astype(float)
                .tolist()
            )


            lows = (
                df["low"]
                .astype(float)
                .tolist()
            )


            closes = (
                df["close"]
                .astype(float)
                .tolist()
            )


            volumes = (
                df["volume"]
                .astype(float)
                .tolist()
            )



            # =============================
            # VWAP
            # =============================

            vwap = (

                self.indicators
                .vwap(

                    closes,

                    volumes

                )

            )



            # =============================
            # SUPERTREND
            # =============================

            supertrend = (

                self.indicators
                .supertrend(

                    highs,

                    lows,

                    closes,

                    SUPERTREND_PERIOD,

                    SUPERTREND_MULTIPLIER

                )

            )



            last_close = closes[-1]

            last_vwap = vwap[-1]

            last_st = supertrend[-1]



            # =============================
            # VOLUME FILTER
            # =============================

            volume_ok = True



            if USE_VOLUME_FILTER:


                avg_volume = (

                    sum(volumes[-20:])

                    /

                    20

                )


                volume_ok = (

                    volumes[-1]

                    >

                    avg_volume *
                    MIN_VOLUME_MULTIPLIER

                )



            if not volume_ok:

                return None




            # =============================
            # ENTRY LONG
            # =============================

            if (

                last_close > last_vwap

                and

                last_close > last_st

            ):


                return {


                    "type":
                        "ENTRY",


                    "side":
                        "Buy",


                    "price":
                        last_close,


                    "strategy":
                        "VWAP_SUPERTREND"

                }





            # =============================
            # ENTRY SHORT
            # =============================

            if (

                last_close < last_vwap

                and

                last_close < last_st

            ):


                return {


                    "type":
                        "ENTRY",


                    "side":
                        "Sell",


                    "price":
                        last_close,


                    "strategy":
                        "VWAP_SUPERTREND"

                }




            # =============================
            # EXIT
            # =============================

            return self.check_exit(

                last_close,

                last_vwap,

                last_st

            )





        except Exception as e:


            print(
                "[STRATEGY ERROR]",
                e
            )


            return None





    # =====================================
    # EXIT
    # =====================================

    def check_exit(

        self,

        price,

        vwap,

        supertrend

    ):



        if (

            price < vwap

            and

            price < supertrend

        ):


            return {


                "type":
                    "EXIT",


                "strategy":
                    "VWAP_SUPERTREND"

            }



        return None





# Singleton

vwap_supertrend_strategy = (
    VWAPSupertrendStrategy()
)
