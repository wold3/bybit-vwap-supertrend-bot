import pandas as pd
import numpy as np


from config import (
    VWAP_LENGTH,
    SUPERTREND_PERIOD,
    SUPERTREND_MULTIPLIER,
)





# ==========================================
# VWAP + SUPERTREND SIGNAL
# ==========================================

class VWAPSupertrend:



    def __init__(self):


        print("==============================")
        print("[SIGNAL INIT]")
        print("VWAP :", VWAP_LENGTH)
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
    # SUPERTREND SIMPLE
    # ======================================

    def calculate_supertrend(

        self,

        high,

        low,

        close

    ):


        df = pd.DataFrame({


            "high": high,


            "low": low,


            "close": close


        })



        df["atr"] = (

            df["high"]

            -

            df["low"]

        ).rolling(

            SUPERTREND_PERIOD

        ).mean()



        df["upper"] = (

            (

                df["high"]

                +

                df["low"]

            )

            /

            2

            +

            df["atr"]

            *

            SUPERTREND_MULTIPLIER

        )



        df["lower"] = (

            (

                df["high"]

                +

                df["low"]

            )

            /

            2

            -

            df["atr"]

            *

            SUPERTREND_MULTIPLIER

        )



        last = df.iloc[-1]



        if close[-1] > last["upper"]:


            return 1



        elif close[-1] < last["lower"]:


            return -1



        return 0





    # ======================================
    # SIGNAL CHECK
    # ======================================

    def check_signal(

        self,

        close,

        volume,

        high,

        low

    ):


        try:


            if len(close) < VWAP_LENGTH:


                print(
                    "[SIGNAL WAIT]",
                    len(close),
                    "/",
                    VWAP_LENGTH
                )


                return None





            price = close[-1]



            vwap = self.calculate_vwap(

                close,

                volume

            )



            trend = self.calculate_supertrend(

                high,

                low,

                close

            )





            print("==============================")
            print("[SIGNAL CHECK]")
            print("PRICE :", price)
            print("VWAP :", round(vwap,2))
            print("SUPERTREND :", trend)
            print("==============================")





            # BUY

            if (

                price > vwap

                and

                trend == 1

            ):


                return "Buy"





            # SELL

            if (

                price < vwap

                and

                trend == -1

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
