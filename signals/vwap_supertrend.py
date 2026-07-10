
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
        candles
    ):


        if len(candles) < VWAP_LENGTH:

            return None



        data = candles[-VWAP_LENGTH:]



        total_volume = 0

        total_price_volume = 0



        for c in data:


            price = (

                c["high"]
                +
                c["low"]
                +
                c["close"]

            ) / 3



            volume = c["volume"]



            total_price_volume += price * volume

            total_volume += volume




        if total_volume == 0:

            return None



        return (

            total_price_volume
            /
            total_volume

        )





    # ======================================
    # ATR
    # ======================================

    def calculate_atr(
        self,
        candles
    ):


        if len(candles) < SUPERTREND_PERIOD + 1:

            return None



        trs = []



        for i in range(1,len(candles)):


            high = candles[i]["high"]

            low = candles[i]["low"]

            prev_close = candles[i-1]["close"]



            tr = max(

                high - low,

                abs(high - prev_close),

                abs(low - prev_close)

            )


            trs.append(tr)



        return np.mean(

            trs[-SUPERTREND_PERIOD:]

        )






    # ======================================
    # SUPERTREND
    # ======================================

    def calculate_supertrend(
        self,
        candles
    ):


        atr = self.calculate_atr(
            candles
        )


        if atr is None:

            return None



        last = candles[-1]



        price = last["close"]



        hl2 = (

            last["high"]
            +
            last["low"]

        ) / 2




        upper = (

            hl2
            +
            atr * SUPERTREND_MULTIPLIER

        )



        lower = (

            hl2
            -
            atr * SUPERTREND_MULTIPLIER

        )





        if price > upper:

            return "UP"



        if price < lower:

            return "DOWN"



        return "NEUTRAL"






    # ======================================
    # SIGNAL
    # ======================================

    def generate_signal(
        self,
        candles
    ):


        if len(candles) < VWAP_LENGTH:

            return "HOLD"



        vwap = self.calculate_vwap(
            candles
        )


        trend = self.calculate_supertrend(
            candles
        )



        if vwap is None or trend is None:

            return "HOLD"




        price = candles[-1]["close"]





        # LONG

        if (

            price > vwap

            and

            trend == "UP"

        ):

            return "BUY"





        # SHORT

        if (

            price < vwap

            and

            trend == "DOWN"

        ):

            return "SELL"





        return "HOLD"







# ==========================================
# SINGLETON
# ==========================================

vwap_supertrend = VWAPSupertrend()
