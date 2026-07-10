# =====================================================
# indicators/indicator_engine.py
# VWAP + SuperTrend Indicator Engine
# =====================================================

import math



from config import (
    ATR_PERIOD,
    SUPERTREND_MULTIPLIER
)







class IndicatorEngine:



    def __init__(self):


        self.candles = []


        self.last_market = None



        print(

            "[INDICATOR ENGINE READY]"

        )







    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        candle
    ):


        self.candles.append(

            candle

        )


        if len(self.candles) > 500:


            self.candles.pop(0)



        self.last_market = (

            self.calculate()

        )



        return self.last_market







    # =====================================================
    # VWAP
    # =====================================================

    def calculate_vwap(self):


        total_volume = 0


        total_price_volume = 0



        for c in self.candles:



            price = (

                c["high"]

                +

                c["low"]

                +

                c["close"]

            ) / 3



            volume = c["volume"]



            total_price_volume += (

                price

                *

                volume

            )


            total_volume += volume





        if total_volume == 0:


            return None



        return (

            total_price_volume

            /

            total_volume

        )







    # =====================================================
    # TRUE RANGE
    # =====================================================

    def true_range(
        self,
        index
    ):


        c = self.candles[index]



        if index == 0:


            return (

                c["high"]

                -

                c["low"]

            )



        prev = self.candles[index-1]



        return max(

            c["high"]

            -

            c["low"],


            abs(

                c["high"]

                -

                prev["close"]

            ),


            abs(

                c["low"]

                -

                prev["close"]

            )

        )







    # =====================================================
    # ATR
    # =====================================================

    def calculate_atr(self):


        if len(self.candles) < ATR_PERIOD + 1:


            return None



        trs = []



        start = (

            len(self.candles)

            -

            ATR_PERIOD

        )



        for i in range(

            start,

            len(self.candles)

        ):


            trs.append(

                self.true_range(i)

            )



        return (

            sum(trs)

            /

            len(trs)

        )







    # =====================================================
    # SUPERTREND
    # =====================================================

    def calculate_supertrend(self):


        atr = self.calculate_atr()



        if atr is None:


            return None



        candle = self.candles[-1]



        hl2 = (

            candle["high"]

            +

            candle["low"]

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



        close = candle["close"]



        if close > upper:


            return "UP"



        elif close < lower:


            return "DOWN"



        else:


            # 이전 방향 유지

            if self.last_market:


                return self.last_market.get(

                    "supertrend"

                )


            return "DOWN"







    # =====================================================
    # CALCULATE ALL
    # =====================================================

    def calculate(self):


        vwap = self.calculate_vwap()



        trend = self.calculate_supertrend()



        return {


            "vwap":

                vwap,


            "supertrend":

                trend,


            "close":

                self.candles[-1]["close"]


        }







    # =====================================================
    # MARKET DATA
    # =====================================================

    def get_market_data(self):


        return self.last_market







# =====================================================
# SINGLETON
# =====================================================

indicator_engine = IndicatorEngine()
