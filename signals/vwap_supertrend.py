import pandas as pd
import numpy as np


from config import (
    VWAP_LENGTH,
    SUPERTREND_PERIOD,
    SUPERTREND_MULTIPLIER,
)



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

    def vwap(

        self,

        close,

        volume

    ):


        close = np.array(close)

        volume = np.array(volume)



        return (

            (close * volume).sum()

            /

            volume.sum()

        )





    # ======================================
    # ATR
    # ======================================

    def atr(

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

            df.high - df.low,


            np.maximum(

                abs(
                    df.high -
                    df.close.shift(1)
                ),


                abs(
                    df.low -
                    df.close.shift(1)
                )

            )

        )


        return (

            df["tr"]

            .rolling(

                SUPERTREND_PERIOD

            )

            .mean()

            .fillna(0)

            .values

        )





    # ======================================
    # SUPERTREND
    # ======================================

    def supertrend(

        self,

        high,

        low,

        close

    ):


        atr = self.atr(

            high,

            low,

            close

        )



        upper = []

        lower = []



        trend = []




        for i in range(len(close)):


            mid = (

                high[i]

                +

                low[i]

            ) / 2



            up = (

                mid

                +

                SUPERTREND_MULTIPLIER

                *

                atr[i]

            )


            dn = (

                mid

                -

                SUPERTREND_MULTIPLIER

                *

                atr[i]

            )



            upper.append(up)

            lower.append(dn)



            if close[i] > up:


                trend.append(1)



            elif close[i] < dn:


                trend.append(-1)



            else:


                if i > 0:


                    trend.append(

                        trend[i-1]

                    )


                else:


                    trend.append(0)





        return trend[-1]





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





            current_vwap = self.vwap(

                close[-VWAP_LENGTH:],

                volume[-VWAP_LENGTH:]

            )



            st = self.supertrend(

                high,

                low,

                close

            )




            print(
                "[SIGNAL CHECK]",
                "PRICE:",
                round(price,2),
                "VWAP:",
                round(current_vwap,2),
                "ST:",
                st
            )





            # LONG

            if (

                price > current_vwap

                and

                st == 1

            ):


                return "Buy"






            # SHORT

            if (

                price < current_vwap

                and

                st == -1

            ):


                return "Sell"






            return None





        except Exception as e:


            print(
                "[SIGNAL ERROR]",
                e
            )


            return None





signal_engine = VWAPSupertrend()
