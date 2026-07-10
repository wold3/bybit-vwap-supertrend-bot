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

        prices,

        volumes

    ):


        if len(prices) < VWAP_LENGTH:

            return None



        prices = np.array(prices[-VWAP_LENGTH:])

        volumes = np.array(volumes[-VWAP_LENGTH:])


        vwap = (

            np.sum(
                prices * volumes
            )

            /

            np.sum(volumes)

        )


        return float(vwap)







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

                high-low,

                abs(high-prev_close),

                abs(low-prev_close)

            )


            tr.append(value)




        atr = np.mean(

            tr[-SUPERTREND_PERIOD:]

        )


        return atr






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





        hl2 = (

            highs[-1]

            +

            lows[-1]

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



        price = closes[-1]



        if price > upper:

            return "UP"



        if price < lower:

            return "DOWN"



        return "NEUTRAL"







    # ======================================
    # SIGNAL GENERATOR
    # ======================================

    def generate_signal(

        self,

        candles

    ):


        try:


            closes = [

                float(x)

                for x in candles["close"]

            ]



            highs = [

                float(x)

                for x in candles["high"]

            ]



            lows = [

                float(x)

                for x in candles["low"]

            ]



            volumes = [

                float(x)

                for x in candles["volume"]

            ]






            current_price = closes[-1]



            vwap = self.calculate_vwap(

                closes,

                volumes

            )



            trend = self.calculate_supertrend(

                highs,

                lows,

                closes

            )





            if vwap is None or trend is None:

                return None





            print(
                "[SIGNAL]",
                "PRICE:",
                current_price,
                "VWAP:",
                round(vwap,2),
                "TREND:",
                trend
            )






            # BUY 조건

            if (

                current_price > vwap

                and

                trend == "UP"

            ):

                return "BUY"






            # SELL 조건

            if (

                current_price < vwap

                and

                trend == "DOWN"

            ):

                return "SELL"






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
