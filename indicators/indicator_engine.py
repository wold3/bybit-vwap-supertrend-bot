import pandas as pd
import numpy as np


class IndicatorEngine:


    def __init__(self):

        self.data = pd.DataFrame(
            columns=[
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume"
            ]
        )


        self.max_candles = 300


        self.last_result = None


        # Supertrend 설정

        self.atr_period = 10
        self.multiplier = 3



        print(
            "[INDICATOR ENGINE READY]"
        )



    # =====================================================
    # UPDATE CANDLE
    # =====================================================

    def update(
        self,
        candle
    ):


        try:


            row = {


                "timestamp":
                int(candle["timestamp"]),


                "open":
                float(candle["open"]),


                "high":
                float(candle["high"]),


                "low":
                float(candle["low"]),


                "close":
                float(candle["close"]),


                "volume":
                float(candle["volume"])

            }



            self.data = pd.concat(

                [

                    self.data,

                    pd.DataFrame(
                        [row]
                    )

                ],

                ignore_index=True

            )



            # 중복 제거

            self.data.drop_duplicates(

                subset=[
                    "timestamp"
                ],

                keep="last",

                inplace=True

            )


            self.data = self.data.tail(
                self.max_candles
            ).reset_index(
                drop=True
            )



            self.calculate()



        except Exception as e:


            print(
                "[INDICATOR UPDATE ERROR]",
                e
            )



    # =====================================================
    # VWAP
    # =====================================================

    def calculate_vwap(self, df):


        typical = (

            df["high"]

            +

            df["low"]

            +

            df["close"]

        ) / 3



        volume = df["volume"]



        vwap = (

            (typical * volume).cumsum()

            /

            volume.cumsum()

        )



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



        prev_close = close.shift(1)



        tr = pd.concat(

            [

                high-low,

                (high-prev_close).abs(),

                (low-prev_close).abs()

            ],

            axis=1

        ).max(
            axis=1
        )



        atr = tr.rolling(

            self.atr_period

        ).mean()



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

            self.multiplier * atr

        )


        lower = (

            hl2

            -

            self.multiplier * atr

        )



        trend = []

        direction = "DOWN"



        for i in range(len(df)):


            close = df["close"].iloc[i]



            if close > upper.iloc[i]:


                direction = "UP"


            elif close < lower.iloc[i]:


                direction = "DOWN"



            trend.append(
                direction
            )



        return trend



    # =====================================================
    # CALCULATE ALL
    # =====================================================

    def calculate(self):


        if len(self.data) < 20:


            return None



        df = self.data.copy()



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



        self.last_result = {


            "vwap":

            float(
                last["vwap"]
            ),


            "supertrend":

            last["trend"],


            "atr":

            float(
                last["atr"]
            )

            if not np.isnan(last["atr"])

            else None,


            "close":

            float(
                last["close"]
            )

        }



        return self.last_result



    # =====================================================
    # GET MARKET DATA
    # =====================================================

    def get_market_data(
        self,
        candle=None
    ):


        return self.last_result





indicator_engine = IndicatorEngine()
