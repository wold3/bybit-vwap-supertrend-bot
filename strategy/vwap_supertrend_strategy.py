# =====================================================
# strategy/vwap_supertrend_strategy.py
# VWAP + SuperTrend Strategy V2
# =====================================================

from config import (
    USE_VOLUME_FILTER,
    MIN_VOLUME_MULTIPLIER
)


from indicators.indicator_engine import (
    indicator_engine
)





class VWAPSuperTrendStrategy:



    def __init__(self, engine):


        self.engine = engine


        self.previous_trend = None


        self.previous_close = None


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
    # NORMALIZE
    # =====================================================

    def normalize_candle(
        self,
        candle
    ):


        return {


            "timestamp":

                int(candle["timestamp"]),


            "open":

                float(candle["open"]),


            "high":

                float(candle["high"]),


            "low":

                float(candle["low"]),


            "close":

                float(candle["close"]),


            "volume":

                float(candle["volume"])

        }







    # =====================================================
    # SIGNAL
    # =====================================================

    def generate_signal(
        self,
        candles
    ):


        try:



            if not candles:


                return None





            clean = []



            for c in candles:


                try:


                    clean.append(

                        self.normalize_candle(c)

                    )


                except:


                    continue





            if len(clean) < 30:


                return None





            self.engine.candles.clear()


            self.engine.last_market = None





            for c in clean:


                self.engine.update(

                    c

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


            close = last["close"]


            volume = last["volume"]






            # =================================================
            # PREVIOUS DATA
            # =================================================

            previous_close = (

                self.previous_close

            )


            previous_trend = (

                self.previous_trend

            )







            # =================================================
            # VOLUME FILTER
            # =================================================

            volume_ok = True



            if USE_VOLUME_FILTER:



                volumes = [

                    x["volume"]

                    for x in clean[-20:]

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


                self.save_state(

                    close,

                    trend

                )


                print(

                    "[NO SIGNAL] VOLUME"

                )


                return None







            # =================================================
            # BUY CONDITION
            # =================================================

            buy = False



            if close > vwap:


                if previous_close:


                    if previous_close <= vwap:


                        buy = True



                if previous_trend == "DOWN" and trend == "UP":


                    buy = True





            if buy:



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



                self.save_state(

                    close,

                    trend

                )


                return signal







            # =================================================
            # SELL CONDITION
            # =================================================

            sell = False



            if close < vwap:



                if previous_close:


                    if previous_close >= vwap:


                        sell = True





                if previous_trend == "UP" and trend == "DOWN":


                    sell = True







            if sell:



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



                self.save_state(

                    close,

                    trend

                )


                return signal






            self.save_state(

                close,

                trend

            )



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
    # SAVE STATE
    # =====================================================

    def save_state(
        self,
        close,
        trend
    ):


        self.previous_close = close


        self.previous_trend = trend







# =====================================================
# SINGLETON
# =====================================================

vwap_supertrend_strategy = VWAPSuperTrendStrategy(

    indicator_engine

)
