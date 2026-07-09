import pandas as pd
import numpy as np


from config import DEFAULT_SYMBOL



class IndicatorEngine:


    def __init__(self):

        self.symbol = DEFAULT_SYMBOL


        self.candles = []


        self.max_length = 200


        self.last = {

            "vwap": None,

            "supertrend": None,

            "atr": None,

        }


        print(
            "[INDICATOR ENGINE READY]"
        )




    # =====================================================
    # UPDATE CANDLE
    # =====================================================


    def update(
        self,
        candle
    ):


        try:


            self.candles.append(

                {

                    "timestamp":
                        candle["timestamp"],

                    "open":
                        float(candle["open"]),

                    "high":
                        float(candle["high"]),

                    "low":
                        float(candle["low"]),

                    "close":
                        float(candle["close"]),

                    "volume":
                        float(candle["volume"]),

                }

            )



            if len(self.candles) > self.max_length:


                self.candles.pop(0)



            self.calculate()



        except Exception as e:


            print(
                "[INDICATOR UPDATE ERROR]",
                e
            )





    # =====================================================
    # CALCULATE
    # =====================================================


    def calculate(self):


        if len(self.candles) < 20:


            return



        df = pd.DataFrame(
            self.candles
        )



        # -------------------------
        # VWAP
        # -------------------------


        price = (

            df["high"]

            +

            df["low"]

            +

            df["close"]

        ) / 3



        volume = df["volume"]



        cumulative_volume = volume.cumsum()



        cumulative_price_volume = (

            price * volume

        ).cumsum()



        vwap = (

            cumulative_price_volume

            /

            cumulative_volume

        )



        current_vwap = float(
            vwap.iloc[-1]
        )



        # -------------------------
        # ATR
        # -------------------------


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

                low_close,

            ],

            axis=1

        ).max(axis=1)



        atr = (

            tr.rolling(14)

            .mean()

        )



        current_atr = float(
            atr.iloc[-1]
        )



        if np.isnan(current_atr):

            return




        # -------------------------
        # Supertrend
        # -------------------------


        multiplier = 3



        hl2 = (

            df["high"]

            +

            df["low"]

        ) / 2



        upper = (

            hl2

            +

            multiplier

            *

            atr

        )



        lower = (

            hl2

            -

            multiplier

            *

            atr

        )



        close = df["close"]



        trend = "UP"



        if close.iloc[-1] < lower.iloc[-1]:


            trend = "DOWN"



        elif close.iloc[-1] > upper.iloc[-1]:


            trend = "UP"



        else:


            previous = self.last.get(
                "supertrend"
            )


            if previous:

                trend = previous




        self.last = {


            "vwap":

                current_vwap,


            "supertrend":

                trend,


            "atr":

                current_atr,


        }



        print(

            "[INDICATORS]",

            self.last

        )





    # =====================================================
    # GET DATA
    # =====================================================


    def get_market_data(
        self,
        candle=None
    ):


        if self.last["vwap"] is None:


            return None



        return {


            "symbol":

                self.symbol,


            "price":

                candle["close"]
                if candle
                else None,


            "vwap":

                self.last["vwap"],


            "supertrend":

                self.last["supertrend"],


            "atr":

                self.last["atr"],

        }






    # =====================================================
    # RESET
    # =====================================================


    def reset(self):


        self.candles.clear()


        self.last = {


            "vwap": None,

            "supertrend": None,

            "atr": None,

        }


        print(
            "[INDICATOR RESET]"
        )






indicator_engine = IndicatorEngine()
