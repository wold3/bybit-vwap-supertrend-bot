# strategy/vwap_supertrend_strategy.py

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


            if candles is None:

                return None



            if len(candles) < 50:

                return None



            df = pd.DataFrame(
                candles
            )



            # ================================
            # DATA TYPE
            # ================================

            for col in [

                "open",
                "high",
                "low",
                "close",
                "volume"

            ]:

                df[col] = (

                    df[col]
                    .astype(float)

                )





            # ================================
            # UPDATE ENGINE
            # ================================

            self.indicator.update(
                df
            )





            # ================================
            # VWAP
            # ================================

            vwap = (

                self.indicator
                .calculate_vwap()

            )





            # ================================
            # SUPERTREND
            # ================================

            supertrend = (

                self.indicator
                .calculate_supertrend()

            )





            # ================================
            # LAST VALUE PARSER
            # ================================

            def last_value(data):


                if isinstance(
                    data,
                    pd.Series
                ):

                    return float(
                        data.iloc[-1]
                    )



                if isinstance(
                    data,
                    pd.DataFrame
                ):

                    return float(
                        data.iloc[-1, -1]
                    )



                if isinstance(
                    data,
                    list
                ):

                    return float(
                        data[-1]
                    )



                return float(data)





            current_vwap = last_value(
                vwap
            )


            current_supertrend = last_value(
                supertrend
            )



            current_price = float(

                df["close"]
                .iloc[-1]

            )





            # ================================
            # VOLUME FILTER
            # ================================

            if USE_VOLUME_FILTER:


                avg_volume = float(

                    df["volume"]
                    .tail(20)
                    .mean()

                )


                current_volume = float(

                    df["volume"]
                    .iloc[-1]

                )



                if current_volume < (

                    avg_volume *
                    MIN_VOLUME_MULTIPLIER

                ):

                    return None





            # ================================
            # LONG ENTRY
            # ================================

            if (

                current_price > current_vwap

                and

                current_price > current_supertrend

            ):


                return {


                    "type":
                    "ENTRY",


                    "side":
                    "Buy",


                    "price":
                    current_price,


                    "strategy":
                    "VWAP_SUPERTREND"

                }





            # ================================
            # SHORT ENTRY
            # ================================

            if (

                current_price < current_vwap

                and

                current_price < current_supertrend

            ):


                return {


                    "type":
                    "ENTRY",


                    "side":
                    "Sell",


                    "price":
                    current_price,


                    "strategy":
                    "VWAP_SUPERTREND"

                }





            # ================================
            # NO SIGNAL
            # ================================

            return None





        except Exception as e:


            print(
                "[STRATEGY ERROR]",
                e
            )


            return None







# Singleton

vwap_supertrend_strategy = (

    VWAPSupertrendStrategy()

)
