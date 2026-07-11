# =====================================================
# strategy/vwap_supertrend.py
# VWAP + SUPERTREND STRATEGY
# =====================================================

import pandas as pd
import numpy as np



from config import (

    ATR_PERIOD,

    SUPERTREND_MULTIPLIER

)







class VWAPSuperTrend:



    def __init__(self):


        self.last_signal = None



        print(

            "[STRATEGY READY]"

        )









    # =====================================================
    # VWAP
    # =====================================================

    def calculate_vwap(

        self,

        df

    ):


        try:


            price = (

                df["close"]

            )


            volume = (

                df["volume"]

            )



            vwap = (

                (price * volume)

                .cumsum()

                /

                volume.cumsum()

            )



            return vwap





        except Exception:


            return None









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

        ).max(

            axis=1

        )



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



        current = 1





        for i in range(

            len(df)

        ):



            if df["close"].iloc[i] > upper.iloc[i]:


                current = 1



            elif df["close"].iloc[i] < lower.iloc[i]:


                current = -1



            trend.append(

                current

            )




        return pd.Series(

            trend,

            index=df.index

        )









    # =====================================================
    # SIGNAL
    # =====================================================

    def generate_signal(

        self,

        df

    ):



        if len(df) < 50:


            return None






        df = df.copy()



        df["vwap"] = self.calculate_vwap(

            df

        )



        df["supertrend"] = self.calculate_supertrend(

            df

        )





        last = df.iloc[-1]





        signal = None






        # BUY

        if (

            last["close"]

            >

            last["vwap"]

            and

            last["supertrend"]

            ==

            1

        ):



            signal = "Buy"







        # SELL

        elif (

            last["close"]

            <

            last["vwap"]

            and

            last["supertrend"]

            ==

            -1

        ):



            signal = "Sell"







        if signal == self.last_signal:


            return None





        self.last_signal = signal



        return signal









# =====================================================
# INSTANCE
# =====================================================

strategy = VWAPSuperTrend()
