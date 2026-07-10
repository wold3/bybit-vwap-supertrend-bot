# =====================================================
# strategy/vwap_supertrend_strategy.py
# VWAP + SuperTrend Strategy
# =====================================================


from config import (
    USE_VOLUME_FILTER,
    MIN_VOLUME_MULTIPLIER,
)


from indicators.indicator_engine import (
    indicator_engine
)



class VWAPSuperTrendStrategy:


    def __init__(self, engine):

        self.engine = engine

        print(
            "[VWAP SUPERTREND STRATEGY READY]"
        )



    # =================================================
    # APP CALL
    # =================================================

    def analyze(self, candles):

        return self.generate_signal(
            candles
        )



    # =================================================
    # SIGNAL
    # =================================================

    def generate_signal(self, candles):

        try:

            if candles is None:

                return None



            if len(candles) < 30:

                return None



            # ---------------------------------
            # Indicator update
            # ---------------------------------

            self.engine.candles.clear()


            for candle in candles:

                self.engine.update(
                    candle
                )



            market = (
                self.engine
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



            # ---------------------------------
            # Volume filter
            # ---------------------------------

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



                if volumes:


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



            print(
                "[INDICATOR]",
                "PRICE:",
                round(close, 2),
                "VWAP:",
                round(vwap, 2),
                "TREND:",
                trend,
                "VOLUME:",
                volume_ok
            )



            if not volume_ok:

                print(
                    "[NO SIGNAL] VOLUME"
                )

                return None



            # ---------------------------------
            # BUY
            # ---------------------------------

            if (

                close > vwap

                and

                trend == "UP"

            ):


                signal = {


                    "signal":
                    "BUY",


                    "side":
                    "Buy",


                    "price":
                    close,


                    "vwap":
                    vwap,


                    "trend":
                    trend

                }


                print(
                    "[SIGNAL BUY]",
                    signal
                )


                return signal



            # ---------------------------------
            # SELL
            # ---------------------------------

            if (

                close < vwap

                and

                trend == "DOWN"

            ):


                signal = {


                    "signal":
                    "SELL",


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
                    "[SIGNAL SELL]",
                    signal
                )


                return signal



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
# =====================================================


vwap_supertrend_strategy = VWAPSuperTrendStrategy(
    indicator_engine
)
