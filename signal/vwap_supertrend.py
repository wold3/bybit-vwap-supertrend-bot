import pandas as pd

from config import (
    VWAP_LENGTH,
    SUPERTREND_PERIOD,
    SUPERTREND_MULTIPLIER,
)


class VWAPSupertrend:


    def __init__(self):

        self.last_signal = None

        print("==============================")
        print("[VWAP SUPERTREND INIT]")
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



    # ==========================================
    # VWAP
    # ==========================================

    def calculate_vwap(self, df):


        price = (

            df["close"]
            +
            df["high"]
            +
            df["low"]

        ) / 3



        volume = df["volume"]



        vwap = (

            price * volume

        ).cumsum() / volume.cumsum()



        return vwap




    # ==========================================
    # ATR
    # ==========================================

    def calculate_atr(self, df):


        high_low = (

            df["high"]
            -
            df["low"]

        )


        high_close = (

            abs(
                df["high"]
                -
                df["close"].shift()
            )

        )


        low_close = (

            abs(
                df["low"]
                -
                df["close"].shift()
            )

        )


        tr = pd.concat(

            [
                high_low,
                high_close,
                low_close
            ],

            axis=1

        ).max(axis=1)



        atr = tr.rolling(

            SUPERTREND_PERIOD

        ).mean()



        return atr




    # ==========================================
    # SUPERTREND
    # ==========================================

    def calculate_supertrend(self, df):


        atr = self.calculate_atr(df)



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


        current = True



        for i in range(len(df)):


            if df["close"].iloc[i] > upper.iloc[i]:

                current = True


            elif df["close"].iloc[i] < lower.iloc[i]:

                current = False



            trend.append(current)



        return pd.Series(trend)




    # ==========================================
    # SIGNAL
    # ==========================================

    def get_signal(self, kline):


        try:


            df = pd.DataFrame(

                kline

            )



            df.columns = [

                "timestamp",
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


                df[col] = pd.to_numeric(

                    df[col]

                )



            if len(df) < 50:

                return "HOLD"



            df["VWAP"] = self.calculate_vwap(df)


            df["TREND"] = self.calculate_supertrend(df)



            last = df.iloc[-1]



            price = float(last["close"])



            # BUY

            if (

                price > last["VWAP"]

                and

                last["TREND"] is True

            ):


                if self.last_signal != "BUY":

                    self.last_signal = "BUY"

                    return "BUY"




            # SELL

            if (

                price < last["VWAP"]

                and

                last["TREND"] is False

            ):


                if self.last_signal != "SELL":

                    self.last_signal = "SELL"

                    return "SELL"




            return "HOLD"



        except Exception as e:


            print(
                "[SIGNAL ERROR]",
                e
            )


            return "HOLD"




# ==========================================
# SINGLETON
# ==========================================

vwap_supertrend = VWAPSupertrend()
