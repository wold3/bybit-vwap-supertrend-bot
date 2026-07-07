import pandas as pd
import numpy as np



class IndicatorEngine:


    def __init__(self):

        self.history = []



    # =====================================
    # UPDATE CANDLE
    # =====================================

    def update(
        self,
        candle
    ):


        self.history.append(

            candle

        )


        # 최근 데이터 유지

        if len(self.history) > 200:

            self.history.pop(0)





    # =====================================
    # VWAP
    # =====================================

    def calculate_vwap(
        self
    ):


        df = pd.DataFrame(

            self.history

        )


        if len(df) == 0:

            return None



        price = (

            df["high"]

            +

            df["low"]

            +

            df["close"]

        ) / 3



        volume = df["volume"]



        vwap = (

            price * volume

        ).sum() / volume.sum()



        return float(vwap)





    # =====================================
    # ATR
    # =====================================

    def atr(
        self,
        period=10
    ):


        df = pd.DataFrame(

            self.history

        )


        high = df["high"]

        low = df["low"]

        close = df["close"]



        tr = pd.concat(

            [

                high-low,


                abs(

                    high-close.shift()

                ),


                abs(

                    low-close.shift()

                )

            ],

            axis=1

        ).max(axis=1)



        atr = tr.rolling(

            period

        ).mean()



        return float(

            atr.iloc[-1]

        )





    # =====================================
    # SUPER TREND
    # =====================================

    def calculate_supertrend(
        self,
        period=10,
        multiplier=3
    ):


        df = pd.DataFrame(

            self.history

        )


        if len(df) < period:

            return None



        current = df.iloc[-1]



        atr = self.atr(

            period

        )



        hl2 = (

            current["high"]

            +

            current["low"]

        ) / 2



        upper = (

            hl2

            +

            multiplier

            *

            atr

        )


        lower = (

            hl2

            -

            multiplier

            *

            atr

        )



        close = current["close"]



        if close > upper:


            return "UP"



        elif close < lower:


            return "DOWN"



        return "UP"





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

                self.calculate_supertrend()

        }





indicator_engine = IndicatorEngine()
