import pandas as pd
import numpy as np


from config import (
    VWAP_LENGTH,
    SUPERTREND_PERIOD,
    SUPERTREND_MULTIPLIER,
)



# ==========================================
# VWAP + SUPERTREND SIGNAL ENGINE
# ==========================================

class VWAPSupertrend:



    def __init__(self):


        print("==============================")
        print("[SIGNAL INIT]")
        print(
            "VWAP :",
            VWAP_LENGTH
        )
        print(
            "SUPERTREND :",
            SUPERTREND_PERIOD,
            SUPERTREND_MULTIPLIER
        )
        print("==============================")





    # ======================================
    # VWAP
    # ======================================

    def calculate_vwap(

        self,

        close,

        volume

    ):


        price_volume = (

            np.array(close)

            *

            np.array(volume)

        )


        return (

            price_volume.sum()

            /

            np.array(volume).sum()

        )





    # ======================================
    # ATR
    # ======================================

    def calculate_atr(

        self,

        high,

        low,

        close

    ):


        df = pd.DataFrame({

            "high":high,

            "low":low,

            "close":close

        })



        df["tr"] = np.maximum(

            df["high"]

            -

            df["low"],


            np.maximum(

                abs(

                    df["high"]

                    -

                    df["close"].shift()

                ),


                abs(

                    df["low"]

                    -

                    df["close"].shift()

                )

            )

        )



        atr = (

            df["tr"]

            .rolling(

                SUPERTREND_PERIOD

            )

            .mean()

            .iloc[-1]

        )


        return atr





    # ======================================
    # SUPERTREND
    # ======================================

    def calculate_supertrend(

        self,

        high,

        low,

        close

    ):


        atr = self.calculate_atr(

            high,

            low,

            close

        )



        if np.isnan(atr):

            return None




        hl2 = (

            high[-1]

            +

            low[-1]

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



        price = close[-1]



        if price > upper:


            return "UP"



        elif price < lower:


            return "DOWN"



        return "NEUTRAL"





    # ======================================
    # SIGNAL
    # ======================================

    def check_signal(

        self,

        close,

        volume,

        high,

        low,

        price=None

    ):


        try:



            if len(close) < VWAP_LENGTH:


                return None




            if price is None:


                price = close[-1]





            vwap = self.calculate_vwap(

                close[-VWAP_LENGTH:],

                volume[-VWAP_LENGTH:]

            )



            trend = self.calculate_supertrend(

                high,

                low,

                close

            )




            print(
                "[SIGNAL CHECK]",
                "PRICE:",
                price,
                "VWAP:",
                round(vwap,2),
                "TREND:",
                trend
            )





            # LONG

            if (

                price > vwap

                and

                trend == "UP"

            ):


                return "Buy"





            # SHORT

            if (

                price < vwap

                and

                trend == "DOWN"

            ):


                return "Sell"





            return None




        except Exception as e:


            print(
                "[SIGNAL ERROR]",
                e
            )


            return None





# ==========================================
# SINGLETON
# ==========================================

signal_engine = VWAPSupertrend()
