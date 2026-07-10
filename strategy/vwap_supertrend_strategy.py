# strategy/vwap_supertrend_strategy.py

from config import (
    USE_VOLUME_FILTER,
    MIN_VOLUME_MULTIPLIER,
)


class VWAPSuperTrendStrategy:


    def __init__(
        self,
        indicator_engine
    ):

        self.indicator_engine = indicator_engine

        print(
            "[VWAP SUPERTREND STRATEGY READY]"
        )



    # ==========================================
    # SIGNAL
    # ==========================================

    def generate_signal(
        self,
        candles
    ):

        try:

            if candles is None:
                return None


            if len(candles) < 20:
                return None



            # ----------------------------------
            # 마지막 캔들
            # ----------------------------------

            candle = candles[-1]


            close = float(
                candle["close"]
            )


            volume = float(
                candle["volume"]
            )



            # ----------------------------------
            # Indicator Update
            # ----------------------------------

            for c in candles:

                self.indicator_engine.update(c)



            vwap = (
                self.indicator_engine
                .calculate_vwap()
            )


            trend = (
                self.indicator_engine
                .calculate_supertrend()
            )



            if vwap is None:
                return None


            if trend is None:
                return None



            vwap = float(vwap)



            # ----------------------------------
            # Volume Filter
            # ----------------------------------

            volume_ok = True


            if USE_VOLUME_FILTER:


                avg_volume = sum(

                    float(
                        x["volume"]
                    )

                    for x in candles[-20:]

                ) / 20



                if volume < (
                    avg_volume
                    *
                    MIN_VOLUME_MULTIPLIER
                ):

                    volume_ok = False



            # ----------------------------------
            # DEBUG
            # ----------------------------------

            print(
                "[INDICATOR]",
                "PRICE:",
                round(close,2),
                "VWAP:",
                round(vwap,2),
                "TREND:",
                trend,
                "VOLUME OK:",
                volume_ok
            )



            if not volume_ok:

                print(
                    "[NO SIGNAL] VOLUME"
                )

                return None



            # ----------------------------------
            # LONG
            # ----------------------------------

            if (

                close > vwap

                and

                trend == "UP"

            ):

                print(
                    "[SIGNAL] LONG"
                )


                return {

                    "side":
                    "Buy",

                    "price":
                    close,

                    "vwap":
                    vwap,

                    "trend":
                    trend

                }



            # ----------------------------------
            # SHORT
            # ----------------------------------

            if (

                close < vwap

                and

                trend == "DOWN"

            ):

                print(
                    "[SIGNAL] SHORT"
                )


                return {

                    "side":
                    "Sell",

                    "price":
                    close,

                    "vwap":
                    vwap,

                    "trend":
                    trend

                }



            print(
                "[NO SIGNAL]"
            )


            return None



        except Exception as e:


            print(
                "[STRATEGY ERROR]",
                e
            )


            return None




# ==========================================
# Singleton
# ==========================================
