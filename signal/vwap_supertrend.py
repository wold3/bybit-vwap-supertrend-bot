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
    # ATR
    # ======================================

    def atr(
        self,
        df,
        period
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



        atr = (
            tr
            .rolling(period)
            .mean()
        )


        return atr




    # ======================================
    # VWAP
    # ======================================

    def calculate_vwap(
        self,
        df
    ):


        price = (
            df["high"]
            +
            df["low"]
            +
            df["close"]
        ) / 3



        volume = df["volume"]



        vwap = (

            price
            *
            volume

        ).rolling(
            VWAP_LENGTH
        ).sum() / volume.rolling(
            VWAP_LENGTH
        ).sum()



        return vwap




    # ======================================
    # SUPERTREND
    # ======================================

    def calculate_supertrend(
        self,
        df
    ):


        atr = self.atr(
            df,
            SUPERTREND_PERIOD
        )


        hl2 = (

            df["high"]
            +
            df["low"]

        ) / 2



        upper = (
            hl2
            +
            (
                SUPERTREND_MULTIPLIER
                *
                atr
            )
        )



        lower = (
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



        for i in range(len(df)):



            if i == 0:

                trend.append(direction)

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




    # ======================================
    # SIGNAL
    # ======================================

    def generate_signal(
        self,
        candles
    ):


        try:


            if candles is None:

                return None



            if len(candles) < 50:

                return None



            df = pd.DataFrame(
                candles
            )



            df.columns = [
                "time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "turnover"
            ]



            for col in [
                "open",
                "high",
                "low",
                "close",
                "volume"
            ]:

                df[col] = (
                    df[col]
                    .astype(float)
                )



            df["vwap"] = (
                self.calculate_vwap(df)
            )


            df["supertrend"] = (
                self.calculate_supertrend(df)
            )



            last = df.iloc[-1]

            previous = df.iloc[-2]



            # =========================
            # LONG
            # =========================

            if (

                previous["close"]
                <
                previous["vwap"]

                and

                last["close"]
                >
                last["vwap"]

                and

                last["supertrend"]
                ==
                1

            ):

                print(
                    "[SIGNAL] LONG"
                )

                return "Buy"




            # =========================
            # SHORT
            # =========================

            if (

                previous["close"]
                >
                previous["vwap"]

                and

                last["close"]
                <
                last["vwap"]

                and

                last["supertrend"]
                ==
                -1

            ):


                print(
                    "[SIGNAL] SHORT"
                )


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

vwap_supertrend = VWAPSupertrend()
