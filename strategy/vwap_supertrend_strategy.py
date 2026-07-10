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
    # VALUE PARSER
    # =====================================

    def last_value(
        self,
        data
    ):


        try:


            # DataFrame

            if isinstance(
                data,
                pd.DataFrame
            ):


                value = data.iloc[-1]


                if isinstance(
                    value,
                    pd.Series
                ):

                    value = value.iloc[-1]


                return float(value)





            # Series

            if isinstance(
                data,
                pd.Series
            ):


                value = data.iloc[-1]


                if isinstance(
                    value,
                    pd.Series
                ):

                    value = value.iloc[-1]


                return float(value)





            # List

            if isinstance(
                data,
                list
            ):


                value = data[-1]


                if isinstance(
                    value,
                    (list, tuple)
                ):

                    value = value[-1]


                return float(value)





            return float(data)



        except Exception as e:


            print(
                "[VALUE PARSE ERROR]",
                e
            )


            return None







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



            # 숫자 변환

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





            # =================================
            # UPDATE ENGINE
            # =================================

            self.indicator.update(
                df
            )





            # =================================
            # INDICATORS
            # =================================

            vwap = (

                self.indicator
                .calculate_vwap()

            )



            supertrend = (

                self.indicator
                .calculate_supertrend()

            )





            current_vwap = self.last_value(
                vwap
            )


            current_supertrend = self.last_value(
                supertrend
            )



            if (

                current_vwap is None

                or

                current_supertrend is None

            ):

                return None





            price = float(

                df["close"]
                .iloc[-1]

            )





            # =================================
            # VOLUME FILTER
            # =================================

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





            # =================================
            # LONG
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
            # SHORT
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







# Singleton

vwap_supertrend_strategy = (

    VWAPSupertrendStrategy()

)
