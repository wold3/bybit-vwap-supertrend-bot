import math
import time
from collections import deque


class IndicatorEngine:


    def __init__(self):

        self.max_length = 200

        self.candles = deque(
            maxlen=self.max_length
        )

        self.last_timestamp = None

        # VWAP
        self.cumulative_volume = 0
        self.cumulative_price_volume = 0

        self.vwap = None


        # Supertrend
        self.atr_period = 10
        self.supertrend_multiplier = 3

        self.atr_values = deque(
            maxlen=self.atr_period
        )

        self.supertrend = None
        self.trend = None


        print("[INDICATOR ENGINE READY]")



    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, candle):


        try:

            timestamp = int(
                candle["timestamp"]
            )


            if timestamp == self.last_timestamp:

                return


            self.last_timestamp = timestamp


            self.candles.append(
                candle
            )


            self.update_vwap()

            self.update_supertrend()



        except Exception as e:

            print(
                "[INDICATOR UPDATE ERROR]",
                e
            )



    # =====================================================
    # VWAP
    # =====================================================

    def update_vwap(self):


        if len(self.candles) == 0:

            return


        candle = self.candles[-1]


        price = (

            candle["high"]

            +

            candle["low"]

            +

            candle["close"]

        ) / 3


        volume = candle["volume"]



        self.cumulative_price_volume += (
            price * volume
        )

        self.cumulative_volume += volume



        if self.cumulative_volume > 0:

            self.vwap = (

                self.cumulative_price_volume

                /

                self.cumulative_volume

            )



    # =====================================================
    # TRUE RANGE
    # =====================================================

    def true_range(self):


        if len(self.candles) < 2:

            return None



        current = self.candles[-1]

        previous = self.candles[-2]



        high = current["high"]

        low = current["low"]

        prev_close = previous["close"]



        tr = max(

            high - low,

            abs(high - prev_close),

            abs(low - prev_close)

        )


        return tr



    # =====================================================
    # ATR
    # =====================================================

    def calculate_atr(self):


        tr = self.true_range()


        if tr is None:

            return None


        self.atr_values.append(
            tr
        )


        if len(self.atr_values) < self.atr_period:

            return None



        return (

            sum(self.atr_values)

            /

            len(self.atr_values)

        )



    # =====================================================
    # SUPERTREND
    # =====================================================

    def update_supertrend(self):


        atr = self.calculate_atr()


        if atr is None:

            return



        candle = self.candles[-1]


        hl2 = (

            candle["high"]

            +

            candle["low"]

        ) / 2



        upper_band = (

            hl2

            +

            self.supertrend_multiplier * atr

        )


        lower_band = (

            hl2

            -

            self.supertrend_multiplier * atr

        )



        close = candle["close"]



        if self.trend is None:

            self.trend = "UP"



        if close > upper_band:

            self.trend = "UP"

            self.supertrend = lower_band



        elif close < lower_band:

            self.trend = "DOWN"

            self.supertrend = upper_band



        else:

            if self.supertrend is None:

                self.supertrend = hl2



    # =====================================================
    # MARKET DATA
    # =====================================================

    def get_market_data(
        self,
        candle=None
    ):


        if self.vwap is None:

            return None


        if self.trend is None:

            return None



        return {


            "timestamp":

                candle.get("timestamp")
                if candle
                else None,


            "close":

                candle.get("close")
                if candle
                else None,


            "vwap":

                self.vwap,


            "supertrend":

                self.trend,


            "supertrend_value":

                self.supertrend,


            "candle_count":

                len(self.candles)

        }



    # =====================================================
    # RESET
    # =====================================================

    def reset(self):


        self.candles.clear()


        self.last_timestamp = None


        self.cumulative_volume = 0

        self.cumulative_price_volume = 0


        self.vwap = None


        self.atr_values.clear()


        self.supertrend = None

        self.trend = None



        print(
            "[INDICATOR RESET]"
        )




indicator_engine = IndicatorEngine()
