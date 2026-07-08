# indicators/indicator_engine.py

import os
import pandas as pd
import numpy as np

from dotenv import load_dotenv


load_dotenv()



class IndicatorEngine:


    def __init__(self):


        self.history = []


        self.supertrend_direction = "UP"


        self.period = int(

            os.getenv(

                "SUPER_TREND_PERIOD",

                "10"

            )

        )


        self.multiplier = float(

            os.getenv(

                "SUPER_TREND_MULTIPLIER",

                "3"

            )

        )


        self.max_history = int(

            os.getenv(

                "MAX_HISTORY",

                "200"

            )

        )





    # =====================================
    # UPDATE CANDLE
    # =====================================

    def update(
        self,
        candle
    ):


        if not candle:

            return



        self.history.append(

            candle

        )



        if len(self.history) > self.max_history:


            self.history.pop(0)





    # =====================================
    # DATAFRAME
    # =====================================

    def dataframe(self):


        if not self.history:

            return None



        return pd.DataFrame(

            self.history

        )





    # =====================================
    # VWAP
    # =====================================

    def calculate_vwap(
        self
    ):


        df = self.dataframe()



        if df is None:

            return None



        typical_price = (

            df["high"]

            +

            df["low"]

            +

            df["close"]

        ) / 3



        volume = df["volume"]



        total_volume = volume.sum()



        if total_volume == 0:

            return float(

                typical_price.iloc[-1]

            )



        return float(

            (

                typical_price

                *

                volume

            ).sum()

            /

            total_volume

        )





    # =====================================
    # ATR
    # =====================================

    def calculate_atr(
        self
    ):


        df = self.dataframe()



        if df is None:

            return None



        if len(df) < self.period:

            return None



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

        ).max(axis=1)



        atr = tr.rolling(

            self.period

        ).mean()



        return float(

            atr.iloc[-1]

        )





    # =====================================
    # SUPER TREND
    # =====================================

    def calculate_supertrend(
        self
    ):


        df = self.dataframe()



        if df is None:

            return None



        if len(df) < self.period:


            return None





        atr = self.calculate_atr()



        if atr is None:

            return None



        current = df.iloc[-1]



        hl2 = (

            current["high"]

            +

            current["low"]

        ) / 2



        upper_band = (

            hl2

            +

            self.multiplier

            *

            atr

        )


        lower_band = (

            hl2

            -

            self.multiplier

            *

            atr

        )



        close = current["close"]



        previous = self.supertrend_direction





        if close > upper_band:


            self.supertrend_direction = "UP"



        elif close < lower_band:


            self.supertrend_direction = "DOWN"



        else:


            self.supertrend_direction = previous





        return self.supertrend_direction





    # =====================================
    # ALL INDICATORS
    # =====================================

    def calculate(
        self
    ):


        return {


            "vwap":

                self.calculate_vwap(),


            "supertrend":

                self.calculate_supertrend(),


            "atr":

                self.calculate_atr()


        }





    # =====================================
    # RESET
    # =====================================

    def reset(self):


        self.history.clear()


        self.supertrend_direction = "UP"





    # =====================================
    # STATUS
    # =====================================

    def status(self):


        return {


            "history":

                len(self.history),


            "supertrend":

                self.supertrend_direction

        }





indicator_engine = IndicatorEngine()
