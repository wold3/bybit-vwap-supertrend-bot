# =====================================================
# strategy/vwap_supertrend_strategy.py
# VWAP + SuperTrend Strategy
# =====================================================

import pandas as pd
import numpy as np





from config import (

    ATR_PERIOD,

    SUPERTREND_MULTIPLIER,

    USE_VOLUME_FILTER,

    VOLUME_PERIOD,

    MIN_VOLUME_MULTIPLIER

)





class VWAPSuperTrendStrategy:


    def __init__(self):


        print(

            "[STRATEGY READY]"

        )









    # =====================================================
    # VWAP
    # =====================================================

    def calculate_vwap(
        self,
        df
    ):


        price = (

            df["close"]

        )


        volume = (

            df["volume"]

        )


        vwap = (

            price

            *

            volume

        ).cumsum() / volume.cumsum()



        return vwap










    # =====================================================
    # ATR
    # =====================================================

    def calculate_atr(
        self,
        df
    ):


        high = df["high"]


        low = df["low"]


        close = df["close"]





        tr1 = high - low


        tr2 = abs(

            high - close.shift()

        )


        tr3 = abs(

            low - close.shift()

        )





        tr = pd.concat(

            [

                tr1,

                tr2,

                tr3

            ],

            axis=1

        ).max(

            axis=1

        )





        atr = (

            tr.rolling(

                ATR_PERIOD

            )

            .mean()

        )



        return atr










    # =====================================================
    # SUPERTREND
    # =====================================================

    def calculate_supertrend(
        self,
        df
    ):


        atr = self.calculate_atr(

            df

        )



        hl2 = (

            df["high"]

            +

            df["low"]

        ) / 2





        upper = (

            hl2

            +

            (

                SUPERTREND_MULTIPLIER

                *

                atr

            )

        )



        lower = (

            hl2

            -

            (

                SUPERTREND_MULTIPLIER

                *

                atr

            )

        )





        trend = []



        current = 1





        for i in range(

            len(df)

        ):


            if df["close"].iloc[i] > upper.iloc[i]:


                current = 1



            elif df["close"].iloc[i] < lower.iloc[i]:


                current = -1





            trend.append(

                current

            )





        return pd.Series(

            trend,

            index=df.index

        )









    # =====================================================
    # VOLUME FILTER
    # =====================================================

    def volume_check(
        self,
        df
    ):


        if not USE_VOLUME_FILTER:


            return True





        avg_volume = (

            df["volume"]

            .rolling(

                VOLUME_PERIOD

            )

            .mean()

            .iloc[-1]

        )



        current = (

            df["volume"]

            .iloc[-1]

        )





        return (

            current

            >=

            avg_volume

            *

            MIN_VOLUME_MULTIPLIER

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





            df = pd.DataFrame(

                candles

            )





            df["vwap"] = (

                self.calculate_vwap(

                    df

                )

            )





            df["trend"] = (

                self.calculate_supertrend(

                    df

                )

            )







            last = df.iloc[-1]


            prev = df.iloc[-2]





            if not self.volume_check(df):


                return None







            signal = None





            # -------------------------
            # BUY
            # -------------------------

            if (

                prev["close"]

                <

                prev["vwap"]

                and

                last["close"]

                >

                last["vwap"]

                and

                last["trend"]

                ==

                1

            ):


                signal = {


                    "signal":

                        "BUY",


                    "price":

                        float(

                            last["close"]

                        ),


                    "vwap":

                        float(

                            last["vwap"]

                        ),


                    "trend":

                        "UP"

                }









            # -------------------------
            # SELL
            # -------------------------

            elif (

                prev["close"]

                >

                prev["vwap"]

                and

                last["close"]

                <

                last["vwap"]

                and

                last["trend"]

                ==

                -1

            ):


                signal = {


                    "signal":

                        "SELL",


                    "price":

                        float(

                            last["close"]

                        ),


                    "vwap":

                        float(

                            last["vwap"]

                        ),


                    "trend":

                        "DOWN"

                }








            return signal







        except Exception as e:


            print(

                "[STRATEGY ERROR]",

                e

            )


            return None










# =====================================================
# INSTANCE
# =====================================================

vwap_supertrend_strategy = VWAPSuperTrendStrategy()
