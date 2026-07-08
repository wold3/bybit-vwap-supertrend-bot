import numpy as np


class Indicators:


    # =====================================================
    # VWAP
    # =====================================================

    def vwap(self, prices, volumes):

        if len(prices) == 0:
            return None

        volume_sum = np.sum(volumes)

        if volume_sum == 0:
            return None

        return np.sum(
            np.array(prices) *
            np.array(volumes)
        ) / volume_sum



    # =====================================================
    # ATR
    # =====================================================

    def atr(
        self,
        highs,
        lows,
        closes,
        period=14
    ):

        if len(closes) < period + 1:
            return None


        tr = []


        for i in range(1, len(closes)):

            high = highs[i]
            low = lows[i]
            prev_close = closes[i-1]


            true_range = max(

                high - low,

                abs(high - prev_close),

                abs(low - prev_close)

            )


            tr.append(true_range)


        return np.mean(
            tr[-period:]
        )



    # =====================================================
    # SUPERTREND
    # =====================================================

    def supertrend(
        self,
        highs,
        lows,
        closes,
        period=10,
        multiplier=3
    ):


        if len(closes) < period + 2:
            return None



        atr_value = self.atr(

            highs,
            lows,
            closes,
            period

        )


        if atr_value is None:
            return None



        hl2 = (

            highs[-1]

            +

            lows[-1]

        ) / 2



        upper_band = (

            hl2

            +

            multiplier * atr_value

        )


        lower_band = (

            hl2

            -

            multiplier * atr_value

        )



        close = closes[-1]



        if close > upper_band:

            return {

                "trend": "UP",

                "direction": 1,

                "value": lower_band

            }



        elif close < lower_band:

            return {

                "trend": "DOWN",

                "direction": -1,

                "value": upper_band

            }



        else:

            return {

                "trend": "NEUTRAL",

                "direction": 0,

                "value": hl2

            }



    # =====================================================
    # TREND STRENGTH
    # =====================================================

    def trend_strength(
        self,
        prices
    ):

        if len(prices) < 30:

            return 0.0


        short = np.mean(
            prices[-10:]
        )


        long = np.mean(
            prices[-30:]
        )


        if long == 0:

            return 0.0


        return abs(
            short - long
        ) / long



# singleton

indicators = Indicators()
