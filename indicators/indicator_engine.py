# =====================================================
# indicators/indicator_engine.py
# VWAP + SuperTrend Indicator Engine
# =====================================================

import math



from config import (
    ATR_PERIOD,
    SUPERTREND_MULTIPLIER,
    VOLUME_PERIOD,
    MIN_VOLUME_MULTIPLIER
)





class IndicatorEngine:



    def __init__(self):


        print(

            "[INDICATOR ENGINE READY]"

        )









    # =====================================================
    # MAIN CALCULATION
    # =====================================================

    def calculate(
        self,
        candles
    ):


        try:


            closes = [

                float(x["close"])

                for x in candles

            ]


            highs = [

                float(x["high"])

                for x in candles

            ]


            lows = [

                float(x["low"])

                for x in candles

            ]


            volumes = [

                float(x["volume"])

                for x in candles

            ]





            vwap = self.calculate_vwap(

                candles

            )





            atr = self.calculate_atr(

                highs,

                lows,

                closes

            )





            trend = self.supertrend(

                highs,

                lows,

                closes,

                atr

            )





            volume_ok = self.volume_filter(

                volumes

            )







            return {


                "vwap":

                    vwap,


                "atr":

                    atr,


                "trend":

                    trend,


                "volume":

                    volume_ok


            }







        except Exception as e:


            print(

                "[INDICATOR ERROR]",

                e

            )


            return {


                "vwap":0,


                "atr":0,


                "trend":"NONE",


                "volume":False


            }









    # =====================================================
    # VWAP
    # =====================================================

    def calculate_vwap(
        self,
        candles
    ):


        total_price_volume = 0


        total_volume = 0





        for c in candles:



            price = (

                float(c["high"])

                +

                float(c["low"])

                +

                float(c["close"])

            ) / 3





            volume = float(

                c["volume"]

            )



            total_price_volume += (

                price *

                volume

            )



            total_volume += volume






        if total_volume == 0:


            return 0





        return (

            total_price_volume

            /

            total_volume

        )









    # =====================================================
    # ATR
    # =====================================================

    def calculate_atr(
        self,
        highs,
        lows,
        closes
    ):


        trs = []



        for i in range(1,len(closes)):



            tr = max(

                highs[i]-lows[i],

                abs(

                    highs[i]-closes[i-1]

                ),

                abs(

                    lows[i]-closes[i-1]

                )

            )


            trs.append(tr)





        if len(trs) < ATR_PERIOD:


            return 0





        return sum(

            trs[-ATR_PERIOD:]

        ) / ATR_PERIOD










    # =====================================================
    # SUPERTREND
    # =====================================================

    def supertrend(
        self,
        highs,
        lows,
        closes,
        atr
    ):



        if atr == 0:


            return "NONE"





        hl2 = (

            highs[-1]

            +

            lows[-1]

        ) / 2





        upper = (

            hl2

            +

            SUPERTREND_MULTIPLIER

            *

            atr

        )





        lower = (

            hl2

            -

            SUPERTREND_MULTIPLIER

            *

            atr

        )





        price = closes[-1]





        if price > upper:


            return "UP"





        if price < lower:


            return "DOWN"





        # 기본 방향 유지


        if closes[-1] >= closes[-2]:


            return "UP"


        else:


            return "DOWN"









    # =====================================================
    # VOLUME FILTER
    # =====================================================

    def volume_filter(
        self,
        volumes
    ):


        if len(volumes) < VOLUME_PERIOD:


            return False





        avg = sum(

            volumes[-VOLUME_PERIOD:]

        ) / VOLUME_PERIOD





        current = volumes[-1]





        if current >= (

            avg *

            MIN_VOLUME_MULTIPLIER

        ):


            return True





        return False










# =====================================================
# SINGLETON
# =====================================================

indicator_engine = IndicatorEngine()
