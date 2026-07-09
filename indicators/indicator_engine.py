import math
from collections import deque


from config import (
    VWAP_LENGTH,
    SUPERTREND_PERIOD,
    SUPERTREND_MULTIPLIER,
)



class IndicatorEngine:


    def __init__(self):

        self.prices = deque(
            maxlen=500
        )

        self.highs = deque(
            maxlen=500
        )

        self.lows = deque(
            maxlen=500
        )

        self.volumes = deque(
            maxlen=500
        )


        self.vwap = None

        self.supertrend = None

        self.atr = None

        self.previous_close = None

        self.last_signal = None



        print("[INDICATOR ENGINE READY]")



    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        candle
    ):


        try:


            close = float(
                candle["close"]
            )

            high = float(
                candle["high"]
            )

            low = float(
                candle["low"]
            )

            volume = float(
                candle["volume"]
            )



            self.prices.append(
                close
            )

            self.highs.append(
                high
            )

            self.lows.append(
                low
            )

            self.volumes.append(
                volume
            )



            self.calculate_vwap()

            self.calculate_supertrend()



        except Exception as e:


            print(
                "[INDICATOR UPDATE ERROR]",
                e
            )




    # =====================================================
    # VWAP
    # =====================================================

    def calculate_vwap(self):


        if len(self.prices) == 0:

            return None



        length = min(

            VWAP_LENGTH,

            len(self.prices)

        )


        prices = list(
            self.prices
        )[-length:]


        volumes = list(
            self.volumes
        )[-length:]



        total_volume = sum(
            volumes
        )



        if total_volume == 0:

            return None



        value = sum(

            p * v

            for p, v in zip(
                prices,
                volumes
            )

        )



        self.vwap = (
            value /
            total_volume
        )


        return self.vwap





    # =====================================================
    # ATR
    # =====================================================

    def calculate_atr(self):


        if len(self.highs) < SUPERTREND_PERIOD + 1:

            return None



        highs = list(
            self.highs
        )

        lows = list(
            self.lows
        )

        closes = list(
            self.prices
        )



        trs = []



        for i in range(
            1,
            len(highs)
        ):


            tr = max(

                highs[i] - lows[i],

                abs(
                    highs[i]
                    -
                    closes[i-1]
                ),

                abs(
                    lows[i]
                    -
                    closes[i-1]
                )

            )


            trs.append(
                tr
            )



        period = SUPERTREND_PERIOD



        if len(trs) < period:

            return None



        self.atr = (

            sum(
                trs[-period:]
            )

            /

            period

        )


        return self.atr





    # =====================================================
    # SUPERTREND
    # =====================================================

    def calculate_supertrend(self):


        atr = self.calculate_atr()


        if atr is None:

            return None



        close = self.prices[-1]



        basic_upper = (

            close

            +

            SUPERTREND_MULTIPLIER
            *
            atr

        )



        basic_lower = (

            close

            -

            SUPERTREND_MULTIPLIER
            *
            atr

        )



        if self.supertrend is None:


            self.supertrend = {

                "upper": basic_upper,

                "lower": basic_lower,

                "trend": "UP"

            }


            return self.supertrend




        previous = self.supertrend



        trend = previous["trend"]



        if close > previous["upper"]:

            trend = "UP"



        elif close < previous["lower"]:

            trend = "DOWN"



        self.supertrend = {


            "upper":
                basic_upper,


            "lower":
                basic_lower,


            "trend":
                trend

        }



        return self.supertrend





    # =====================================================
    # MARKET DATA
    # =====================================================

    def get_market_data(
        self,
        candle=None
    ):


        if self.vwap is None:

            return None


        if self.supertrend is None:

            return None



        return {


            "close":

                float(
                    candle["close"]
                )
                if candle
                else None,


            "vwap":

                self.vwap,


            "supertrend":

                self.supertrend["trend"],


            "atr":

                self.atr,


        }





indicator_engine = IndicatorEngine()
