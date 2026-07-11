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


            price = df["close"]

            volume = df["volume"]



            cumulative_volume = volume.cumsum()



            if cumulative_volume.iloc[-1] == 0:


                return None



            vwap = (

                (price * volume)

                .cumsum()

                /

                cumulative_volume

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

    def calculate_atr(

        self,

        df

    ):


        try:


            high = df["high"]

            low = df["low"]

            close = df["close"]



            tr1 = high - low


            tr2 = (

                high - close.shift()

            ).abs()


            tr3 = (

                low - close.shift()

            ).abs()



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

                tr

                .rolling(

                    ATR_PERIOD

                )

                .mean()

                .fillna(0)

            )



            return atr



        except Exception as e:


            print(

                "[ATR ERROR]",

                e

            )


            return None





    # =====================================================
    # SUPERTREND
    # =====================================================

    def calculate_supertrend(

        self,

        df

    ):


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




            upper_band = (

                hl2

                +

                (

                    SUPERTREND_MULTIPLIER

                    *

                    atr

                )

            )



            lower_band = (

                hl2

                -

                (

                    SUPERTREND_MULTIPLIER

                    *

                    atr

                )

            )




            trend = []



            direction = 1




            for i in range(

                len(df)

            ):



                close = df["close"].iloc[i]



                if close > upper_band.iloc[i]:


                    direction = 1



                elif close < lower_band.iloc[i]:


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
    # GENERATE SIGNAL
    # =====================================================

    def generate_signal(

        self,

        df

    ):


        try:


            if df is None:


                return None



            if len(df) < 50:


                return None




            data = df.copy()




            data["vwap"] = self.calculate_vwap(

                data

            )



            data["supertrend"] = self.calculate_supertrend(

                data

            )





            if (

                data["vwap"] is None

                or

                data["supertrend"] is None

            ):


                return None




            # ---------------------------------
            # CLOSED CANDLE
            # ---------------------------------

            candle = data.iloc[-2]



            signal = None




            # ---------------------------------
            # BUY
            # ---------------------------------

            if (

                candle["close"]

                >

                candle["vwap"]

                and

                candle["supertrend"]

                ==

                1

            ):


                signal = "Buy"





            # ---------------------------------
            # SELL
            # ---------------------------------

            elif (

                candle["close"]

                <

                candle["vwap"]

                and

                candle["supertrend"]

                ==

                -1

            ):


                signal = "Sell"





            # ---------------------------------
            # DUPLICATE BLOCK
            # ---------------------------------

            if signal is None:


                return None



            if signal == self.last_signal:


                return None





            self.last_signal = signal



            print(

                "[STRATEGY SIGNAL]",

                signal

            )



            return signal





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
