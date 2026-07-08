import pandas as pd
import threading



class IndicatorEngine:
    """
    Indicator Engine

    기능:
    - Candle 저장
    - VWAP 계산
    - ATR 계산
    - Supertrend 계산
    - Strategy Engine용 market_data 생성
    """



    def __init__(self):

        self.lock = threading.Lock()

        self.history = []

        self.max_history = 200





    # =====================================
    # UPDATE CANDLE
    # =====================================

    def update(
        self,
        candle
    ):


        if not candle:

            return None



        with self.lock:


            self.history.append(

                candle

            )


            if len(self.history) > self.max_history:

                self.history.pop(0)



            result = {


                "symbol":

                    candle.get(
                        "symbol"
                    ),


                "close":

                    candle.get(
                        "close"
                    ),


                "vwap":

                    self.calculate_vwap(),


                "supertrend":

                    self.calculate_supertrend()

            }



            return result





    # =====================================
    # VWAP
    # =====================================

    def calculate_vwap(
        self
    ):


        if not self.history:

            return None



        df = pd.DataFrame(

            self.history

        )



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

                df["close"].iloc[-1]

            )



        return float(

            (

                typical_price * volume

            ).sum()

            /

            total_volume

        )





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



        if len(df) < period + 1:

            return None



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



        return float(

            tr.rolling(

                period

            ).mean().iloc[-1]

        )





    # =====================================
    # SUPER TREND
    # =====================================

    def calculate_supertrend(
        self,
        period=10,
        multiplier=3
    ):


        if len(self.history) < period:

            return "FLAT"



        df = pd.DataFrame(

            self.history

        )



        atr = self.atr(

            period

        )



        if atr is None:

            return "FLAT"



        current = df.iloc[-1]



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



        if close < lower:

            return "DOWN"



        # 기존 전략과 호환

        return "UP"





    # =====================================
    # STATUS
    # =====================================

    def status(
        self
    ):


        with self.lock:


            return {


                "history":

                    len(self.history),


                "latest":

                    self.history[-1]

                    if self.history

                    else None

            }





# singleton

indicator_engine = IndicatorEngine()
