# =====================================================
# indicators/indicator_engine.py
# VWAP + SuperTrend Indicator Engine
# =====================================================

import math



from config import (
    ATR_PERIOD,
    SUPERTREND_MULTIPLIER,
    VWAP_PERIOD
)







class IndicatorEngine:



    def __init__(self):


        self.candles = []


        self.last_market = None



        print(

            "[INDICATOR ENGINE READY]"

        )







    # =====================================================
    # UPDATE CANDLE
    # =====================================================

    def update(
        self,
        candle
    ):


        try:


            self.candles.append(

                candle

            )



            if len(self.candles) > 500:


                self.candles.pop(

                    0

                )



            self.calculate()



        except Exception as e:


            print(

                "[INDICATOR UPDATE ERROR]",

                e

            )







    # =====================================================
    # CALCULATE
    # =====================================================

    def calculate(self):


        if len(self.candles) < ATR_PERIOD + 5:


            return None



        vwap = self.calculate_vwap()



        atr = self.calculate_atr()



        trend = self.calculate_supertrend(

            atr

        )



        self.last_market = {


            "vwap":

                vwap,


            "atr":

                atr,


            "supertrend":

                trend


        }



        return self.last_market







    # =====================================================
    # VWAP
    # =====================================================

    def calculate_vwap(self):


        candles = self.candles[-VWAP_PERIOD:]



        total_volume = 0


        total_price_volume = 0



        for c in candles:


            typical = (


                c["high"]

                +

                c["low"]

                +

                c["close"]

            ) / 3




            volume = c["volume"]



            total_price_volume += (

                typical

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
        current,
        previous
    ):


        if previous is None:


            return (

                current["high"]

                -

                current["low"]

            )



        return max(


            current["high"]

            -

            current["low"],



            abs(

                current["high"]

                -

                previous["close"]

            ),



            abs(

                current["low"]

                -

                previous["close"]

            )


        )







    # =====================================================
    # ATR
    # =====================================================

    def calculate_atr(self):


        trs = []



        candles = self.candles[-(ATR_PERIOD+1):]



        for i in range(

            len(candles)

        ):


            previous = None



            if i > 0:


                previous = candles[i-1]



            trs.append(

                self.true_range(

                    candles[i],

                    previous

                )

            )





        if len(trs) < ATR_PERIOD:


            return None




        return sum(

            trs[-ATR_PERIOD:]

        ) / ATR_PERIOD







    # =====================================================
    # SUPERTREND
    # =====================================================

    def calculate_supertrend(
        self,
        atr
    ):


        if atr is None:


            return None



        candle = self.candles[-1]



        close = candle["close"]



        hl2 = (


            candle["high"]

            +

            candle["low"]

        ) / 2




        upper = (

            hl2

            +

            (

                SUPERTREND_MULTIPLIER

                *

                atr

            )

        )



        lower = (

            hl2

            -

            (

                SUPERTREND_MULTIPLIER

                *

                atr

            )

        )




        if close > upper:


            return "UP"



        if close < lower:


            return "DOWN"




        # 이전 추세 유지


        if self.last_market:


            return self.last_market.get(

                "supertrend"

            )



        return "DOWN"







    # =====================================================
    # MARKET DATA
    # =====================================================

    def get_market_data(self):


        return self.last_market







    # =====================================================
    # RESET
    # =====================================================

    def reset(self):


        self.candles.clear()


        self.last_market = None







# =====================================================
# SINGLETON
# =====================================================

indicator_engine = IndicatorEngine()
