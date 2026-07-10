from strategy.indicators import indicators

from config import (
    ST_LENGTH,
    ST_MULTIPLIER,
    USE_VOLUME_FILTER,
    MIN_VOLUME_MULTIPLIER,
)



class VWAPSuperTrendStrategy:


    def __init__(self):


        self.position = None


        self.last_trend = 0




    # ======================================
    # ANALYZE
    # ======================================

    def analyze(
        self,
        candles
    ):


        if not candles:

            return None



        if len(candles) < ST_LENGTH + 20:

            return None



        closes = [

            float(c["close"])

            for c in candles

        ]


        highs = [

            float(c["high"])

            for c in candles

        ]


        lows = [

            float(c["low"])

            for c in candles

        ]


        volumes = [

            float(c["volume"])

            for c in candles

        ]



        # ==========================
        # INDICATORS
        # ==========================


        vwap = indicators.vwap(

            closes,

            volumes

        )



        supertrend = indicators.supertrend(

            highs,

            lows,

            closes,

            ST_LENGTH,

            ST_MULTIPLIER

        )



        if supertrend is None:

            return None



        trend = supertrend["direction"]



        price = closes[-1]



        current_volume = volumes[-1]


        avg_volume = sum(

            volumes[-20:]

        ) / 20



        # ==========================
        # VOLUME FILTER
        # ==========================


        if USE_VOLUME_FILTER:


            if current_volume < (

                avg_volume *

                MIN_VOLUME_MULTIPLIER

            ):

                return None




        # ==========================
        # ENTRY
        # ==========================


        # SuperTrend 변경 확인


        trend_changed = (

            trend != self.last_trend

        )


        self.last_trend = trend




        # LONG


        if (

            trend == 1

            and

            trend_changed

            and

            price > vwap

            and

            self.position != "Buy"

        ):



            self.position = "Buy"



            return {


                "type":

                "ENTRY",


                "side":

                "Buy",


                "price":

                price,


                "vwap":

                vwap,


                "trend":

                trend


            }




        # SHORT


        if (

            trend == -1

            and

            trend_changed

            and

            price < vwap

            and

            self.position != "Sell"

        ):



            self.position = "Sell"



            return {


                "type":

                "ENTRY",


                "side":

                "Sell",


                "price":

                price,


                "vwap":

                vwap,


                "trend":

                trend


            }




        # ==========================
        # EXIT
        # ==========================


        if self.position == "Buy":


            if trend == -1:



                old = self.position


                self.position = None



                return {


                    "type":

                    "EXIT",


                    "side":

                    old


                }




        if self.position == "Sell":


            if trend == 1:



                old = self.position


                self.position = None



                return {


                    "type":

                    "EXIT",


                    "side":

                    old


                }




        return None





vwap_supertrend_strategy = VWAPSuperTrendStrategy()
