# =====================================================
# strategy/vwap_supertrend.py
# VWAP + SUPERTREND AUTO TRADING STRATEGY
# =====================================================


import pandas as pd
import numpy as np



from config import (

    ATR_PERIOD,

    SUPERTREND_MULTIPLIER,

    VWAP_LENGTH

)







class VWAPSuperTrend:



    def __init__(self):


        self.last_signal = None

        self.last_candle = None


        print(

            "[VWAP SUPERTREND READY]"

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



        pv = typical * df["volume"]



        return (

            pv.rolling(

                VWAP_LENGTH

            )

            .sum()

            /

            df["volume"]

            .rolling(

                VWAP_LENGTH

            )

            .sum()

        )









    # =====================================================
    # ATR
    # =====================================================

    def calculate_atr(self, df):


        high = df["high"]

        low = df["low"]

        close = df["close"]



        tr = pd.concat(

            [

                high-low,

                (high-close.shift()).abs(),

                (low-close.shift()).abs()

            ],

            axis=1

        ).max(axis=1)



        return tr.rolling(

            ATR_PERIOD

        ).mean()










    # =====================================================
    # SUPERTREND
    # =====================================================

    def calculate_supertrend(self,df):


        atr = self.calculate_atr(df)


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


        direction = 1



        for i in range(len(df)):



            if i == 0:


                trend.append(1)

                continue




            close = df["close"].iloc[i]



            if close > upper.iloc[i-1]:

                direction = 1



            elif close < lower.iloc[i-1]:

                direction = -1





            trend.append(direction)





        return pd.Series(

            trend,

            index=df.index

        )









    # =====================================================
    # SIGNAL
    # =====================================================

    def generate_signal(self,df):


        try:



            if df is None:

                return None



            if len(df)<100:

                return None




            data=df.copy()



            data["vwap"] = self.calculate_vwap(

                data

            )


            data["trend"] = self.calculate_supertrend(

                data

            )





            # 마지막 확정 캔들

            candle=data.iloc[-2]

            prev=data.iloc[-3]





            if pd.isna(candle["vwap"]):

                return None





            timestamp=candle["timestamp"]



            if timestamp == self.last_candle:

                return None






            self.last_candle=timestamp





            signal=None





            # =========================
            # BUY CROSS
            # =========================

            if (

                prev["close"] <= prev["vwap"]

                and

                candle["close"] > candle["vwap"]

                and

                candle["trend"] == 1

            ):


                signal="Buy"







            # =========================
            # SELL CROSS
            # =========================

            elif (

                prev["close"] >= prev["vwap"]

                and

                candle["close"] < candle["vwap"]

                and

                candle["trend"] == -1

            ):


                signal="Sell"








            if signal:


                if signal != self.last_signal:


                    self.last_signal=signal



                    print(

                        "[AUTO SIGNAL]",

                        signal,

                        candle["close"]

                    )



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


strategy = VWAPSuperTrend()
