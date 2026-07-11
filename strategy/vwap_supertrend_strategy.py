# =====================================================
# strategy/vwap_supertrend_strategy.py
# VWAP + SuperTrend Strategy
# =====================================================

import pandas as pd
import numpy as np


from config import (
    ATR_PERIOD,
    SUPERTREND_MULTIPLIER,
    VOLUME_PERIOD,
    MIN_VOLUME_MULTIPLIER,
    USE_VOLUME_FILTER
)





class VWAPSuperTrendStrategy:


    def __init__(self):


        self.last_signal = None


        self.last_indicator = {}



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


        if len(candles) < 50:


            return None





        df = pd.DataFrame(

            candles

        )



        df = self.calculate_vwap(

            df

        )


        df = self.calculate_atr(

            df

        )


        df = self.calculate_supertrend(

            df

        )







        last = df.iloc[-1]





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

                avg_volume *

                MIN_VOLUME_MULTIPLIER

            )








        self.last_indicator = {


            "vwap":

                round(

                    last["vwap"],

                    2

                ),


            "trend":

                last["trend"],


            "volume":

                volume_ok

        }







        print(

            "[INDICATOR]",

            "PRICE:",

            last["close"],

            "VWAP:",

            round(

                last["vwap"],

                2

            ),

            "TREND:",

            last["trend"],

            "VOLUME:",

            volume_ok

        )








        if USE_VOLUME_FILTER and not volume_ok:


            print(

                "[NO SIGNAL] VOLUME"

            )


            return None







        signal = None





        # ==============================
        # BUY
        # ==============================


        if (

            last["close"]

            >

            last["vwap"]

            and

            last["trend"]

            ==

            "UP"

        ):



            signal = {


                "signal":

                    "BUY",


                "side":

                    "Buy",


                "reason":

                    "VWAP UP + SUPERTREND"

            }








        # ==============================
        # SELL
        # ==============================


        elif (

            last["close"]

            <

            last["vwap"]

            and

            last["trend"]

            ==

            "DOWN"

        ):



            signal = {


                "signal":

                    "SELL",


                "side":

                    "Sell",


                "reason":

                    "VWAP DOWN + SUPERTREND"

            }









        if signal:


            if signal["signal"] == self.last_signal:


                return None



            self.last_signal = signal["signal"]



            return signal







        return None










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



        df["vwap"] = (

            (

                price *

                volume

            )

            .cumsum()

            /

            volume

            .cumsum()

        )



        return df







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





        tr1 = (

            high -

            low

        )



        tr2 = abs(

            high -

            close.shift()

        )



        tr3 = abs(

            low -

            close.shift()

        )



        tr = pd.concat(

            [

                tr1,

                tr2,

                tr3

            ],

            axis=1

        ).max(axis=1)





        df["atr"] = (

            tr

            .rolling(

                ATR_PERIOD

            )

            .mean()

        )



        return df







    # =====================================================
    # SUPERTREND
    # =====================================================


    def calculate_supertrend(
        self,
        df
    ):


        hl2 = (

            df["high"]

            +

            df["low"]

        ) / 2





        upper = (

            hl2

            +

            SUPERTREND_MULTIPLIER *

            df["atr"]

        )



        lower = (

            hl2

            -

            SUPERTREND_MULTIPLIER *

            df["atr"]

        )





        trend = []



        current = "UP"





        for i in range(

            len(df)

        ):



            if df["close"].iloc[i] > upper.iloc[i]:


                current = "UP"



            elif df["close"].iloc[i] < lower.iloc[i]:


                current = "DOWN"



            trend.append(

                current

            )





        df["trend"] = trend



        return df







# =====================================================
# INSTANCE
# =====================================================


vwap_supertrend_strategy = VWAPSuperTrendStrategy()
