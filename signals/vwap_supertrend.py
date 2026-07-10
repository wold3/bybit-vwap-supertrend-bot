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
        prices,
        volumes
    ):


        if len(prices) < VWAP_LENGTH:

            return None



        prices = np.array(prices[-VWAP_LENGTH:])

        volumes = np.array(volumes[-VWAP_LENGTH:])


        total_volume = volumes.sum()


        if total_volume == 0:

            return None



        vwap = (

            prices * volumes

        ).sum() / total_volume



        return float(vwap)



    # ======================================
    # ATR
    # ======================================

    def calculate_atr(
        self,
        prices
    ):


        if len(prices) < SUPERTREND_PERIOD + 1:

            return None



        highs = np.array(
            prices[-SUPERTREND_PERIOD:]
        )


        lows = highs.copy()



        tr = highs.max() - lows.min()


        atr = tr / SUPERTREND_PERIOD



        return atr



    # ======================================
    # SUPERTREND
    # ======================================

    def calculate_supertrend(
        self,
        prices
    ):


        if len(prices) < SUPERTREND_PERIOD:

            return None



        atr = self.calculate_atr(
            prices
        )


        if atr is None:

            return None



        current = prices[-1]



        upper = (

            current

            +

            atr * SUPERTREND_MULTIPLIER

        )


        lower = (

            current

            -

            atr * SUPERTREND_MULTIPLIER

        )



        if current > lower:

            return "UP"



        if current < upper:

            return "DOWN"



        return None



    # ======================================
    # SIGNAL CHECK
    # ======================================

    def check_signal(
        self,
        prices,
        volumes=None
    ):


        try:


            if len(prices) < VWAP_LENGTH:

                return None



            if volumes is None:

                volumes = [

                    1

                    for _ in prices

                ]



            vwap = self.calculate_vwap(

                prices,

                volumes

            )



            trend = self.calculate_supertrend(

                prices

            )



            if vwap is None:

                return None



            current = prices[-1]



            # LONG

            if (

                current > vwap

                and

                trend == "UP"

            ):

                return "Buy"



            # SHORT

            if (

                current < vwap

                and

                trend == "DOWN"

            ):

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

signal_engine = VWAPSupertrend()
