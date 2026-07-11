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





class VWAPSupertrendStrategy:


    def __init__(self):


        self.last_signal = None


        self.last_indicator = {}


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



        return (

            (price * volume)

            .cumsum()

            /

            volume.cumsum()

        )









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





        tr = pd.concat(

            [

                high-low,


                abs(high-close.shift()),


                abs(low-close.shift())

            ],

            axis=1

        ).max(

            axis=1

        )



        atr = (

            tr

            .rolling(

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

            SUPERTREND_MULTIPLIER

            *

            atr

        )




        lower = (

            hl2

            -

            SUPERTREND_MULTIPLIER

            *

            atr

        )





        trend = []



        direction = True





        for i in range(

            len(df)

        ):


            price = df["close"].iloc[i]



            if price > upper.iloc[i]:


                direction = True



            elif price < lower.iloc[i]:


                direction = False





            trend.append(

                "UP"

                if direction

                else

                "DOWN"

            )



        return trend










    # =====================================================
    # ANALYZE
    # =====================================================


    def analyze(
        self,
        candles
    ):


        try:


            df = pd.DataFrame(

                candles

            )



            if len(df) < 50:


                return None







            df["vwap"] = self.calculate_vwap(

                df

            )



            df["atr"] = self.calculate_atr(

                df

            )



            df["trend"] = self.calculate_supertrend(

                df

            )







            last = df.iloc[-1]

            prev = df.iloc[-2]







            # Volume Filter


            volume_ok = True



            if USE_VOLUME_FILTER:


                avg_volume = (

                    df["volume"]

                    .rolling(

                        VOLUME_PERIOD

                    )

                    .mean()

                    .iloc[-1]

                )


                volume_ok = (

                    last["volume"]

                    >

                    avg_volume

                    *

                    MIN_VOLUME_MULTIPLIER

                )









            self.last_indicator = {


                "vwap":

                    round(

                        float(last["vwap"]),

                        2

                    ),


                "trend":

                    last["trend"],


                "volume":

                    volume_ok

            }








            signal = None







            # ==========================
            # BUY CONDITION
            # ==========================


            if (

                last["close"]

                >

                last["vwap"]

                and

                last["trend"]

                ==

                "UP"

                and

                volume_ok

                and

                prev["close"]

                <=

                prev["vwap"]

            ):


                signal = {


                    "signal":

                        "BUY",


                    "side":

                        "Buy",


                    "price":

                        float(last["close"])

                }







            # ==========================
            # SELL CONDITION
            # ==========================


            elif (

                last["close"]

                <

                last["vwap"]

                and

                last["trend"]

                ==

                "DOWN"

                and

                volume_ok

                and

                prev["close"]

                >=

                prev["vwap"]

            ):


                signal = {


                    "signal":

                        "SELL",


                    "side":

                        "Sell",


                    "price":

                        float(last["close"])

                }








            if signal:


                if signal["signal"] == self.last_signal:


                    return None



                self.last_signal = signal["signal"]



                return signal





            return None







        except Exception as e:


            print(

                "[STRATEGY ERROR]",

                e

            )


            return None







# =====================================================
# INSTANCE
# =====================================================


vwap_supertrend_strategy = VWAPSupertrendStrategy()
