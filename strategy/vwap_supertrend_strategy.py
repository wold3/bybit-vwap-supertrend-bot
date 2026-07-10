import pandas as pd


from config import (
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


            if not candles:

                return None



            if len(candles) < 50:

                return None



            df = pd.DataFrame(
                candles
            )


            df["open"] = df["open"].astype(float)

            df["high"] = df["high"].astype(float)

            df["low"] = df["low"].astype(float)

            df["close"] = df["close"].astype(float)

            df["volume"] = df["volume"].astype(float)



            # =================================
            # UPDATE INDICATOR ENGINE
            # =================================

            self.indicator.update(
                df
            )



            # =================================
            # VWAP
            # =================================

            vwap = (

                self.indicator
                .calculate_vwap()

            )



            # =================================
            # SUPERTREND
            # =================================

            supertrend = (

                self.indicator
                .calculate_supertrend()

            )



            price = (

                float(
                    df["close"]
                    .iloc[-1]
                )

            )



            current_vwap = (

                float(
                    vwap
                    if isinstance(vwap, (int,float))
                    else vwap[-1]
                )

            )



            current_supertrend = (

                float(
                    supertrend
                    if isinstance(supertrend, (int,float))
                    else supertrend[-1]
                )

            )



            # =================================
            # VOLUME FILTER
            # =================================

            if USE_VOLUME_FILTER:


                avg_volume = (

                    df["volume"]
                    .tail(20)
                    .mean()

                )


                if (

                    df["volume"]
                    .iloc[-1]

                    <

                    avg_volume *
                    MIN_VOLUME_MULTIPLIER

                ):

                    return None





            # =================================
            # LONG ENTRY
            # =================================

            if (

                price > current_vwap

                and

                price > current_supertrend

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





            # =================================
            # SHORT ENTRY
            # =================================

            if (

                price < current_vwap

                and

                price < current_supertrend

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
