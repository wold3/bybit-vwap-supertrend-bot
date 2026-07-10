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
    # VWAP 계산
    # ======================================

    def calculate_vwap(
        self,
        prices,
        volumes
    ):


        if len(prices) == 0:

            return None


        volume_sum = np.sum(volumes)


        if volume_sum == 0:

            return None



        return np.sum(
            np.array(prices)
            *
            np.array(volumes)
        ) / volume_sum



    # ======================================
    # ATR 계산
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
    # Supertrend 계산
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



        basis = np.mean(
            prices[-SUPERTREND_PERIOD:]
        )



        upper_band = (

            basis
            +
            atr * SUPERTREND_MULTIPLIER

        )



        lower_band = (

            basis
            -
            atr * SUPERTREND_MULTIPLIER

        )



        current = prices[-1]



        if current > upper_band:

            return "BUY"



        elif current < lower_band:

            return "SELL"



        return "HOLD"



    # ======================================
    # Signal 생성
    # ======================================

    def generate_signal(
        self,
        prices,
        volumes
    ):


        if len(prices) < VWAP_LENGTH:

            return None



        vwap = self.calculate_vwap(

            prices[-VWAP_LENGTH:],

            volumes[-VWAP_LENGTH:]

        )



        if vwap is None:

            return None



        trend = self.calculate_supertrend(

            prices

        )



        current = prices[-1]



        # LONG

        if (

            current > vwap

            and

            trend == "BUY"

        ):

            return "BUY"



        # SHORT

        if (

            current < vwap

            and

            trend == "SELL"

        ):

            return "SELL"



        return None




    # ======================================
    # MAIN LOOP 연결 함수
    # ======================================

    def check_signal(
        self,
        candles
    ):


        try:


            prices = []

            volumes = []



            for candle in candles:


                if isinstance(candle, dict):


                    prices.append(

                        float(
                            candle["close"]
                        )

                    )


                    volumes.append(

                        float(
                            candle["volume"]
                        )

                    )


                else:


                    # Bybit kline 배열 대응
                    # [
                    # timestamp,
                    # open,
                    # high,
                    # low,
                    # close,
                    # volume
                    # ]

                    prices.append(

                        float(
                            candle[4]
                        )

                    )


                    volumes.append(

                        float(
                            candle[5]
                        )

                    )



            return self.generate_signal(

                prices,

                volumes

            )



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
