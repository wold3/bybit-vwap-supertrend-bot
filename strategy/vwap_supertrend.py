# =====================================================
# strategy/vwap_supertrend.py
# VWAP + SUPERTREND STRATEGY
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

            "[STRATEGY READY]"

        )





    # =====================================================
    # VWAP
    # =====================================================


    def calculate_vwap(self, df):


        try:


            price = (

                df["high"]

                +

                df["low"]

                +

                df["close"]

            ) / 3



            volume = df["volume"]



            pv = price * volume



            vwap = (


                pv

                .rolling(

                    VWAP_LENGTH

                )

                .sum()


                /


                volume

                .rolling(

                    VWAP_LENGTH

                )

                .sum()

            )



            return vwap



        except Exception as e:


            print(

                "[VWAP ERROR]",

                e

            )


            return None







    # =====================================================
    # ATR
    # =====================================================


    def calculate_atr(self, df):


        try:


            high = df["high"]

            low = df["low"]

            close = df["close"]



            tr = pd.concat(

                [

                    high - low,


                    (high - close.shift()).abs(),


                    (low - close.shift()).abs()


                ],

                axis=1

            ).max(axis=1)



            atr = tr.rolling(

                ATR_PERIOD

            ).mean()



            return atr.fillna(0)



        except Exception as e:


            print(

                "[ATR ERROR]",

                e

            )


            return None







    # =====================================================
    # SUPERTREND
    # =====================================================


    def calculate_supertrend(self, df):


        try:


            atr = self.calculate_atr(

                df

            )



            if atr is None:


                return None





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





            final_upper = upper.copy()

            final_lower = lower.copy()



            trend = []



            direction = 1





            for i in range(

                len(df)

            ):



                if i == 0:


                    trend.append(

                        direction

                    )

                    continue





                if df["close"].iloc[i] > final_upper.iloc[i-1]:


                    direction = 1



                elif df["close"].iloc[i] < final_lower.iloc[i-1]:


                    direction = -1




                trend.append(

                    direction

                )





            return pd.Series(

                trend,

                index=df.index

            )



        except Exception as e:


            print(

                "[SUPERTREND ERROR]",

                e

            )


            return None







    # =====================================================
    # SIGNAL
    # =====================================================


    def generate_signal(self, df):


        try:


            if df is None:


                return None



            if len(df) < 50:


                return None





            data = df.copy()



            data["vwap"] = self.calculate_vwap(

                data

            )



            data["trend"] = self.calculate_supertrend(

                data

            )





            candle = data.iloc[-2]





            timestamp = candle["timestamp"]





            if timestamp == self.last_candle:


                return None





            signal = None





            # BUY

            if (

                candle["close"]

                >

                candle["vwap"]

                and

                candle["trend"]

                ==

                1

            ):


                signal = "Buy"





            # SELL


            elif (

                candle["close"]

                <

                candle["vwap"]

                and

                candle["trend"]

                ==

                -1

            ):


                signal = "Sell"







            self.last_candle = timestamp





            if signal != self.last_signal:


                self.last_signal = signal


                if signal:


                    print(

                        "[SIGNAL]",

                        signal

                    )


                    return signal






            return None





        except Exception as e:


            print(

                "[SIGNAL ERROR]",

                e

            )


            return None






# =====================================================
# INSTANCE
# =====================================================


strategy = VWAPSuperTrend()
