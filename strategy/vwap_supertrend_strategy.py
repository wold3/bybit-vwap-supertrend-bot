# =====================================================
# strategy/vwap_supertrend_strategy.py
# VWAP + SuperTrend Strategy
# =====================================================


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



    # =================================================
    # SIGNAL GENERATOR
    # =================================================

    def generate_signal(
        self,
        candles
    ):

        try:

            if candles is None:
                return None


            if len(candles) < 30:
                return None



            # -----------------------------------------
            # Indicator update
            # -----------------------------------------

            self.indicator_engine.candles.clear()


            for candle in candles:

                self.indicator_engine.update(
                    candle
                )



            market = (

                self.indicator_engine
                .get_market_data()

            )



            if market is None:

                return None



            vwap = market.get(
                "vwap"
            )


            trend = market.get(
                "supertrend"
            )



            if vwap is None:
                return None


            if trend is None:
                return None



            candle = candles[-1]



            close = float(
                candle["close"]
            )


            volume = float(
                candle["volume"]
            )



            vwap = float(
                vwap
            )



            # -----------------------------------------
            # Volume Filter
            # -----------------------------------------

            volume_ok = True



            if USE_VOLUME_FILTER:


                volumes = []


                for c in candles[-20:]:

                    try:

                        volumes.append(
                            float(
                                c["volume"]
                            )
                        )

                    except:

                        pass



                if len(volumes) > 0:


                    avg_volume = (

                        sum(volumes)

                        /

                        len(volumes)

                    )


                    if volume < (

                        avg_volume

                        *

                        MIN_VOLUME_MULTIPLIER

                    ):

                        volume_ok = False



            # -----------------------------------------
            # DEBUG
            # -----------------------------------------

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



            # -----------------------------------------
            # LONG
            # -----------------------------------------

            if (

                close > vwap

                and

                trend == "UP"

            ):


                print(
                    "[SIGNAL] LONG"
                )


                return {


                    "signal":
                    "LONG",


                    "side":
                    "Buy",


                    "price":
                    close,


                    "vwap":
                    vwap,


                    "trend":
                    trend

                }



            # -----------------------------------------
            # SHORT
            # -----------------------------------------

            if (

                close < vwap

                and

                trend == "DOWN"

            ):


                print(
                    "[SIGNAL] SHORT"
                )


                return {


                    "signal":
                    "SHORT",


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





# =====================================================
# Singleton
# app.py 호환용
# =====================================================


from indicators.indicator_engine import (
    indicator_engine
)



vwap_supertrend_strategy = VWAPSuperTrendStrategy(
    indicator_engine
)
