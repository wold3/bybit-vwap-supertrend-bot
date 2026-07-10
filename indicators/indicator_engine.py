import pandas as pd
import numpy as np



class IndicatorEngine:


    def __init__(self):


        self.length = 100


        self.period = 10

        self.multiplier = 3



        self.df = pd.DataFrame()



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

                    candle["timestamp"],


                "open":

                    candle["open"],


                "high":

                    candle["high"],


                "low":

                    candle["low"],


                "close":

                    candle["close"],


                "volume":

                    candle["volume"],


            }





            self.df = pd.concat(

                [

                    self.df,

                    pd.DataFrame(
                        [row]
                    )

                ],

                ignore_index=True

            )





            if len(self.df) > self.length:


                self.df = (

                    self.df

                    .iloc[
                        -self.length:
                    ]

                    .reset_index(
                        drop=True
                    )

                )





            self.calculate()



        except Exception as e:


            print(
                "[INDICATOR UPDATE ERROR]",
                e
            )









    # =====================================================
    # CALCULATE
    # =====================================================

    def calculate(self):


        if len(self.df) < 20:


            return






        df = self.df






        # -------------------------
        # VWAP
        # -------------------------


        price = (

            df["close"]

        )



        volume = (

            df["volume"]

        )



        df["vwap"] = (

            (

                price * volume

            )

            .cumsum()

            /

            volume.cumsum()

        )






        # -------------------------
        # ATR
        # -------------------------


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

                self.period

            )

            .mean()

        )



        df["atr"] = atr






        # -------------------------
        # SuperTrend
        # -------------------------


        hl2 = (

            high + low

        ) / 2





        upper = (

            hl2

            +

            self.multiplier

            *

            atr

        )





        lower = (

            hl2

            -

            self.multiplier

            *

            atr

        )



        trend = []



        current = "UP"




        for i in range(
            len(df)
        ):


            if i == 0:


                trend.append(
                    current
                )

                continue




            if close.iloc[i] > upper.iloc[i-1]:


                current = "UP"



            elif close.iloc[i] < lower.iloc[i-1]:


                current = "DOWN"




            trend.append(
                current
            )




        df["supertrend"] = trend




        self.df = df







    # =====================================================
    # GET DATA
    # =====================================================

    def get_market_data(
        self,
        candle=None
    ):


        try:


            if len(self.df) == 0:


                return None






            last = self.df.iloc[-1]





            vwap = last.get(
                "vwap"
            )


            trend = last.get(
                "supertrend"
            )





            if pd.isna(vwap):


                return None






            return {


                "vwap":

                    float(vwap),


                "supertrend":

                    trend,


            }






        except Exception as e:


            print(
                "[MARKET DATA ERROR]",
                e
            )


            return None







indicator_engine = IndicatorEngine()
