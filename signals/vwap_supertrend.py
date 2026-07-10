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

    def calculate_vwap(self, prices, volumes):

        if len(prices) == 0:
            return None


        pv = np.array(prices) * np.array(volumes)

        return (
            pv.sum()
            /
            np.array(volumes).sum()
        )



    # ======================================
    # ATR
    # ======================================

    def calculate_atr(
        self,
        prices,
        period=None
    ):

        if period is None:
            period = SUPERTREND_PERIOD


        if len(prices) < period + 1:

            return None


        tr = []


        for i in range(1, len(prices)):

            tr.append(
                abs(
                    prices[i]
                    -
                    prices[i-1]
                )
            )


        return np.mean(
            tr[-period:]
        )



    # ======================================
    # SUPERTREND
    # ======================================

    def calculate_supertrend(
        self,
        prices
    ):


        atr = self.calculate_atr(
            prices
        )


        if atr is None:

            return None



        middle = np.mean(
            prices[-SUPERTREND_PERIOD:]
        )


        upper = (
            middle
            +
            atr * SUPERTREND_MULTIPLIER
        )


        lower = (
            middle
            -
            atr * SUPERTREND_MULTIPLIER
        )


        current = prices[-1]


        if current > upper:

            return "BUY"


        elif current < lower:

            return "SELL"


        return "HOLD"



    # ======================================
    # MAIN SIGNAL
    # ======================================

    def generate_signal(
        self,
        prices,
        volumes
    ):


        if len(prices) < VWAP_LENGTH:

            return "HOLD"



        vwap = self.calculate_vwap(
            prices[-VWAP_LENGTH:],
            volumes[-VWAP_LENGTH:]
        )


        supertrend = self.calculate_supertrend(
            prices
        )


        current = prices[-1]



        if (
            current > vwap
            and supertrend == "BUY"
        ):

            return "Buy"



        if (
            current < vwap
            and supertrend == "SELL"
        ):

            return "Sell"



        return "HOLD"




# ==========================================
# SINGLETON
# ==========================================

signal_engine = VWAPSupertrend()
