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


        vwap = (

            (price * volume).cumsum()

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

            ATR_PERIOD

        ).mean()



        return atr







    # =====================================================
    # SUPERTREND
    # =====================================================


    def calculate_supertrend(
        self,
        df
    ):


        atr = (

            self.calculate_atr(

                df

            )

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



        current = "DOWN"





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



        return trend







    # =====================================================
    # ANALYZE
    # =====================================================


    def analyze(
        self,
        candles
    ):


        try:


            if len(candles) < 50:


                return None






            df = pd.DataFrame(

                candles

            )



            df["vwap"] = (

                self.calculate_vwap(

                    df

                )

            )




            df["trend"] = (

                self.calculate_supertrend(

                    df

                )

            )







            last = df.iloc[-1]



            price = float(

                last["close"]

            )


            vwap = float(

                last["vwap"]

            )


            trend = last["trend"]







            # ==========================
            # Volume Filter
            # ==========================


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

                        vwap,

                        2

                    ),


                "trend":

                    trend,


                "volume":

                    volume_ok

            }







            print(

                "[INDICATOR]",

                "PRICE:",

                price,

                "VWAP:",

                round(vwap,2),

                "TREND:",

                trend,

                "VOLUME:",

                volume_ok

            )









            if USE_VOLUME_FILTER and not volume_ok:


                print(

                    "[NO SIGNAL] VOLUME"

                )


                return None







            # ==========================
            # BUY
            # ==========================


            if (

                price > vwap

                and

                trend == "UP"

            ):


                if self.last_signal != "BUY":


                    self.last_signal = "BUY"



                    return {


                        "signal":

                            "BUY",


                        "side":

                            "Buy",


                        "reason":

                            "VWAP + SUPERTREND"

                    }









            # ==========================
            # SELL
            # ==========================


            if (

                price < vwap

                and

                trend == "DOWN"

            ):


                if self.last_signal != "SELL":


                    self.last_signal = "SELL"



                    return {


                        "signal":

                            "SELL",


                        "side":

                            "Sell",


                        "reason":

                            "VWAP + SUPERTREND"

                    }







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


vwap_supertrend_strategy = VWAPSuperTrendStrategy()
