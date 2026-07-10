# =====================================================
# indicators/indicator_engine.py
# VWAP + SuperTrend Engine
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



            if len(self.candles) > 300:


                self.candles.pop(0)





            self.last_market = (

                self.calculate()

            )





        except Exception as e:


            print(

                "[INDICATOR UPDATE ERROR]",

                e

            )








    # =====================================================
    # MARKET DATA
    # =====================================================

    def get_market_data(self):


        return self.last_market







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



        return {


            "vwap":

            vwap,


            "atr":

            atr,


            "supertrend":

            trend


        }








    # =====================================================
    # VWAP
    # =====================================================

    def calculate_vwap(self):


        total_price_volume = 0


        total_volume = 0




        for c in self.candles:



            price = (

                (

                    c["high"]

                    +

                    c["low"]

                    +

                    c["close"]

                )

                /

                3

            )



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

    def calculate_atr(self):


        trs = []



        candles = self.candles



        for i in range(

            1,

            len(candles)

        ):



            high = candles[i]["high"]


            low = candles[i]["low"]


            prev_close = candles[i-1]["close"]





            tr = max(


                high-low,


                abs(high-prev_close),


                abs(low-prev_close)


            )



            trs.append(

                tr

            )





        if len(trs) < ATR_PERIOD:


            return None





        recent = trs[-ATR_PERIOD:]



        return sum(recent) / ATR_PERIOD









    # =====================================================
    # SUPERTREND
    # =====================================================

    def calculate_supertrend(
        self,
        atr
    ):


        try:



            candle = self.candles[-1]



            close = candle["close"]



            basic_upper = (

                (

                    candle["high"]

                    +

                    candle["low"]

                )

                /

                2

                +

                SUPERTREND_MULTIPLIER

                *

                atr

            )




            basic_lower = (

                (

                    candle["high"]

                    +

                    candle["low"]

                )

                /

                2

                -

                SUPERTREND_MULTIPLIER

                *

                atr

            )





            if close > basic_upper:


                return "UP"




            elif close < basic_lower:


                return "DOWN"





            else:


                # 이전 방향 유지

                if self.last_market:


                    return self.last_market.get(

                        "supertrend",

                        "UP"

                    )



                return "UP"





        except Exception as e:



            print(

                "[SUPERTREND ERROR]",

                e

            )


            return None







# =====================================================
# SINGLETON
# =====================================================

indicator_engine = IndicatorEngine()
