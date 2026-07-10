# =====================================================
# indicators/indicator_engine.py
# VWAP + ATR + SuperTrend Engine
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



        if len(self.candles) > 300:


            self.candles.pop(0)









    # =====================================================
    # VWAP
    # =====================================================

    def calculate_vwap(self):


        try:


            total_volume = 0


            total_price_volume = 0





            for c in self.candles:



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






        except Exception as e:


            print(

                "[VWAP ERROR]",

                e

            )


            return None










    # =====================================================
    # ATR
    # =====================================================

    def calculate_atr(self):


        try:



            if len(self.candles) < ATR_PERIOD + 1:


                return None






            trs = []





            for i in range(

                1,

                len(self.candles)

            ):


                current = self.candles[i]


                previous = self.candles[i-1]




                tr = max(


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



                trs.append(

                    tr

                )







            atr = sum(

                trs[-ATR_PERIOD:]

            ) / ATR_PERIOD





            return atr






        except Exception as e:


            print(

                "[ATR ERROR]",

                e

            )


            return None










    # =====================================================
    # SUPERTREND
    # =====================================================

    def calculate_supertrend(self):


        try:


            atr = self.calculate_atr()



            if atr is None:


                return None





            last = self.candles[-1]



            close = last["close"]





            hl2 = (

                last["high"]

                +

                last["low"]

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




            elif close < lower:


                return "DOWN"





            # 기본 방향 유지

            if self.last_market:


                return self.last_market.get(

                    "supertrend"

                )




            return "UP"






        except Exception as e:


            print(

                "[SUPERTREND ERROR]",

                e

            )


            return None










    # =====================================================
    # MARKET DATA
    # =====================================================

    def get_market_data(self):


        try:



            if len(self.candles) < 30:


                return None






            vwap = self.calculate_vwap()



            trend = self.calculate_supertrend()



            atr = self.calculate_atr()






            if vwap is None:


                return None





            self.last_market = {


                "vwap":

                    vwap,


                "supertrend":

                    trend,


                "atr":

                    atr,


                "price":

                    self.candles[-1]["close"]

            }





            return self.last_market





        except Exception as e:


            print(

                "[MARKET DATA ERROR]",

                e

            )


            return None







# =====================================================
# SINGLETON
# =====================================================

indicator_engine = IndicatorEngine()
