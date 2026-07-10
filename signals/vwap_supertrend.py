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
        closes,
        volumes
    ):


        if len(closes) < VWAP_LENGTH:

            return None



        closes = np.array(
            closes[-VWAP_LENGTH:]
        )


        volumes = np.array(
            volumes[-VWAP_LENGTH:]
        )



        return (

            np.sum(
                closes * volumes
            )
            /
            np.sum(volumes)

        )




    # ======================================
    # ATR
    # ======================================

    def calculate_atr(
        self,
        highs,
        lows,
        closes
    ):


        if len(closes) < SUPERTREND_PERIOD + 1:

            return None



        tr = []



        for i in range(1, len(closes)):


            high = highs[i]

            low = lows[i]

            prev_close = closes[i-1]



            value = max(

                high - low,

                abs(high - prev_close),

                abs(low - prev_close)

            )


            tr.append(value)



        return np.mean(

            tr[-SUPERTREND_PERIOD:]

        )




    # ======================================
    # SUPERTREND
    # ======================================

    def calculate_supertrend(
        self,
        highs,
        lows,
        closes
    ):


        atr = self.calculate_atr(

            highs,

            lows,

            closes

        )


        if atr is None:

            return None



        last_close = closes[-1]

        middle = (

            highs[-1]

            +

            lows[-1]

        ) / 2



        upper = (

            middle

            +

            SUPERTREND_MULTIPLIER * atr

        )



        lower = (

            middle

            -

            SUPERTREND_MULTIPLIER * atr

        )



        if last_close > upper:

            return "UP"



        if last_close < lower:

            return "DOWN"



        return "NEUTRAL"




    # ======================================
    # SIGNAL CHECK
    # ======================================

    def check_signal(
        self,
        prices,
        volumes,
        highs=None,
        lows=None,
        closes=None
    ):



        if len(prices) < VWAP_LENGTH:

            return None



        if highs is None:

            highs = prices

        if lows is None:

            lows = prices

        if closes is None:

            closes = prices




        vwap = self.calculate_vwap(

            closes,

            volumes

        )



        trend = self.calculate_supertrend(

            highs,

            lows,

            closes

        )



        if vwap is None:

            return None



        current = closes[-1]



        print(

            "[SIGNAL CHECK]",

            "PRICE:",
            round(current,2),

            "VWAP:",
            round(vwap,2),

            "TREND:",
            trend

        )




        # BUY

        if (

            current > vwap

            and

            trend == "UP"

        ):

            return "Buy"




        # SELL

        if (

            current < vwap

            and

            trend == "DOWN"

        ):

            return "Sell"



        return None





# ==========================================
# SINGLETON
# ==========================================

signal_engine = VWAPSupertrend()
