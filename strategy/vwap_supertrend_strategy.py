import pandas as pd


from config import (
    VWAP_LENGTH,

    ST_LENGTH,
    SUPERTREND_PERIOD,
    SUPERTREND_MULTIPLIER,

    USE_VOLUME_FILTER,
    MIN_VOLUME_MULTIPLIER
)


from indicators.indicator_engine import (
    IndicatorEngine
)



class VWAPSupertrendStrategy:


    def __init__(self):

        self.indicator = IndicatorEngine()



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



            # ==========================
            # VWAP
            # ==========================

            vwap = (

                self.indicator
                .vwap(

                    closes,

                    volumes

                )

            )



            # ==========================
            # SUPERTREND
            # ==========================

            supertrend = (

                self.indicator
                .supertrend(

                    highs,

                    lows,

                    closes,

                    ST_LENGTH,

                    SUPERTREND_MULTIPLIER

                )

            )



            price = closes[-1]

            current_vwap = vwap[-1]

            current_st = supertrend[-1]



            # ==========================
            # VOLUME FILTER
            # ==========================

            if USE_VOLUME_FILTER:


                avg_volume = (

                    sum(volumes[-VWAP_LENGTH:])

                    /

                    VWAP_LENGTH

                )


                if volumes[-1] < (

                    avg_volume *
                    MIN_VOLUME_MULTIPLIER

                ):

                    return None





            # ==========================
            # LONG
            # ==========================

            if (

                price > current_vwap

                and

                price > current_st

            ):


                return {


                    "type":
                    "ENTRY",


                    "side":
                    "Buy",


                    "price":
                    price,


                    "strategy":
                    "VWAP_SUPERTREND"

                }





            # ==========================
            # SHORT
            # ==========================

            if (

                price < current_vwap

                and

                price < current_st

            ):


                return {


                    "type":
                    "ENTRY",


                    "side":
                    "Sell",


                    "price":
                    price,


                    "strategy":
                    "VWAP_SUPERTREND"

                }





            return None





        except Exception as e:


            print(
                "[STRATEGY ERROR]",
                e
            )


            return None





vwap_supertrend_strategy = (
    VWAPSupertrendStrategy()
)
