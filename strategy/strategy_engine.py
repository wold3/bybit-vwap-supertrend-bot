import pandas as pd
import numpy as np


class IndicatorEngine:


    def __init__(self):

        # symbol별 candle 저장
        self.history = {}



    # =====================================
    # UPDATE CANDLE
    # =====================================

    def update(
        self,
        candle
    ):

        symbol = candle.get("symbol")


        if not symbol:

            return None



        # symbol 초기화

        if symbol not in self.history:

            self.history[symbol] = []



        self.history[symbol].append(

            candle

        )


        # 최근 200개 candle 유지

        if len(self.history[symbol]) > 200:

            self.history[symbol].pop(0)



        indicators = self.calculate(

            symbol

        )



        if not indicators:

            return None



        market_data = {


            "symbol":

                symbol,


            "close":

                candle["close"],


            "volume":

                candle["volume"],


            "timestamp":

                candle["timestamp"],



            # StrategyEngine 입력 형식

            "vwap":

                indicators["vwap"],



            "supertrend":

                indicators["supertrend"]

        }



        return market_data





    # =====================================
    # VWAP
    # =====================================

    def calculate_vwap(
        self,
        symbol
    ):


        candles = self.history.get(

            symbol

        )


        if not candles:

            return None



        df = pd.DataFrame(

            candles

        )



        price = (

            df["high"]

            +

            df["low"]

            +

            df["close"]

        ) / 3



        volume = df["volume"]



        if volume.sum() == 0:

            return None



        vwap = (

            price * volume

        ).sum() / volume.sum()



        return float(vwap)





    # =====================================
    # ATR
    # =====================================

    def atr(
        self,
        symbol,
        period=10
    ):


        candles = self.history.get(

            symbol

        )


        if not candles:

            return None



        df = pd.DataFrame(

            candles

        )



        high = df["high"]

        low = df["low"]

        close = df["close"]



        tr = pd.concat(

            [

                high - low,


                abs(

                    high - close.shift()

                ),


                abs(

                    low - close.shift()

                )

            ],

            axis=1

        ).max(axis=1)



        atr = tr.rolling(

            period

        ).mean()



        value = atr.iloc[-1]



        if np.isnan(value):

            return None



        return float(value)





    # =====================================
    # SUPER TREND
    # =====================================

    def calculate_supertrend(
        self,
        symbol,
        period=10,
        multiplier=3
    ):


        candles = self.history.get(

            symbol

        )


        if not candles:

            return None



        if len(candles) < period:

            return None



        df = pd.DataFrame(

            candles

        )



        current = df.iloc[-1]



        atr = self.atr(

            symbol,

            period

        )


        if atr is None:

            return None



        hl2 = (

            current["high"]

            +

            current["low"]

        ) / 2



        upper = (

            hl2

            +

            multiplier * atr

        )



        lower = (

            hl2

            -

            multiplier * atr

        )



        close = current["close"]



        if close > upper:

            return "UP"



        elif close < lower:

            return "DOWN"



        else:

            return "FLAT"





    # =====================================
    # ALL INDICATORS
    # =====================================

    def calculate(
        self,
        symbol
    ):


        return {


            "vwap":

                self.calculate_vwap(

                    symbol

                ),



            "supertrend":

                self.calculate_supertrend(

                    symbol

                )

        }





# Singleton

indicator_engine = IndicatorEngine()
