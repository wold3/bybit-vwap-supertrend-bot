# =====================================================
# strategy/vwap_supertrend_strategy.py
# VWAP + SuperTrend Trading Strategy
# =====================================================


from config import (
    USE_VOLUME_FILTER,
    MIN_VOLUME_MULTIPLIER,
)


from indicators.indicator_engine import (
    indicator_engine
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
    # ANALYZE
    # app.py 호출용
    # =================================================

    def analyze(
        self,
        candles
    ):


        return self.generate_signal(
            candles
        )



    # =================================================
    # SIGNAL
    # =================================================

    def generate_signal(
        self,
        candles
    ):


        try:


            if candles is None:
                return None



            if len(candles) < 50:

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



                if len(volumes):


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


                        print(
                            "[NO SIGNAL] LOW VOLUME"
                        )


                        return None



            # -----------------------------------------
            # LOG
            # -----------------------------------------

            print(
                "[INDICATOR]",
                "PRICE:",
                round(close,2),
                "VWAP:",
                round(vwap,2),
                "TREND:",
                trend
            )



            # -----------------------------------------
            # LONG ENTRY
            # -----------------------------------------

            if (

                close > vwap

                and

                trend == "UP"

            ):


                signal = {


                    "signal":
                    "LONG",


                    "side":
                    "Buy",


                    "entry":
                    close,


                    "price":
                    close,


                    "vwap":
                    vwap,


                    "trend":
                    trend

                }



                print(
                    "[SIGNAL LONG]",
                    signal
                )


                return signal




            # -----------------------------------------
            # SHORT ENTRY
            # -----------------------------------------

            if (

                close < vwap

                and

                trend == "DOWN"

            ):


                signal = {


                    "signal":
                    "SHORT",


                    "side":
                    "Sell",


                    "entry":
                    close,


                    "price":
                    close,


                    "vwap":
                    vwap,


                    "trend":
                    trend

                }



                print(
                    "[SIGNAL SHORT]",
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
