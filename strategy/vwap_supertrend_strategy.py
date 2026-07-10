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





    # =====================================================
    # APP ENTRY
    # =====================================================

    def analyze(
        self,
        candles
    ):


        return self.generate_signal(

            candles

        )





    # =====================================================
    # NORMALIZE CANDLE
    # =====================================================

    def normalize_candle(
        self,
        candle
    ):


        return {


            "timestamp":

                int(

                    candle["timestamp"]

                ),


            "open":

                float(

                    candle["open"]

                ),


            "high":

                float(

                    candle["high"]

                ),


            "low":

                float(

                    candle["low"]

                ),


            "close":

                float(

                    candle["close"]

                ),


            "volume":

                float(

                    candle["volume"]

                )

        }





    # =====================================================
    # SIGNAL GENERATOR
    # =====================================================

    def generate_signal(
        self,
        candles
    ):


        try:



            if not candles:


                return None




            if len(candles) < 30:


                return None





            clean = []



            for c in candles:


                try:


                    clean.append(

                        self.normalize_candle(c)

                    )


                except Exception:


                    continue





            if len(clean) < 30:


                return None





            # reset engine


            self.engine.candles.clear()


            self.engine.last_market = None





            for candle in clean:


                self.engine.update(

                    candle

                )





            market = (

                self.engine
                .get_market_data()

            )





            if not market:


                return None





            vwap = market.get(

                "vwap"

            )


            trend = market.get(

                "supertrend"

            )





            if vwap is None or trend is None:


                return None





            last = clean[-1]



            close = float(

                last["close"]

            )


            volume = float(

                last["volume"]

            )



            vwap = float(

                vwap

            )





            # =================================================
            # VOLUME FILTER
            # =================================================


            volume_ok = True



            if USE_VOLUME_FILTER:


                volumes = [



                    float(c["volume"])

                    for c in clean[-20:]


                ]



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

                round(close,2),

                "VWAP:",

                round(vwap,2),

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





            # =================================================
            # BUY
            # =================================================


            if close > vwap and trend == "UP":



                signal = {


                    "signal":

                        "BUY",


                    "type":

                        "ENTRY",


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





            # =================================================
            # SELL
            # =================================================


            if close < vwap and trend == "DOWN":



                signal = {


                    "signal":

                        "SELL",


                    "type":

                        "ENTRY",


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
# SINGLETON
# =====================================================


vwap_supertrend_strategy = VWAPSuperTrendStrategy(

    indicator_engine

)
