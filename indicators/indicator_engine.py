from collections import deque
import math


from config import (
    VWAP_LENGTH,
    SUPERTREND_PERIOD,
    SUPERTREND_MULTIPLIER,
)





class IndicatorEngine:



    def __init__(self):


        self.candles = deque(

            maxlen=200

        )



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



        if len(self.candles) < SUPERTREND_PERIOD + 2:


            return None





        vwap = self.calculate_vwap()



        trend = self.calculate_supertrend()






        self.last_market = {


            "vwap":

                vwap,


            "supertrend":

                trend,


        }



        return self.last_market










    # =====================================================
    # VWAP
    # =====================================================

    def calculate_vwap(self):


        data = list(
            self.candles
        )[-VWAP_LENGTH:]



        total_volume = 0


        total_value = 0






        for c in data:



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



            total_value += (

                price

                *

                volume

            )



            total_volume += volume






        if total_volume == 0:


            return None






        return round(

            total_value / total_volume,

            2

        )









    # =====================================================
    # ATR
    # =====================================================

    def calculate_atr(self):


        data = list(
            self.candles
        )



        trs = []





        for i in range(

            1,

            len(data)

        ):



            high = float(

                data[i]["high"]

            )


            low = float(

                data[i]["low"]

            )


            prev_close = float(

                data[i-1]["close"]

            )



            tr = max(


                high - low,


                abs(high - prev_close),


                abs(low - prev_close),


            )



            trs.append(
                tr
            )







        if len(trs) < SUPERTREND_PERIOD:


            return None






        atr = sum(

            trs[-SUPERTREND_PERIOD:]

        ) / SUPERTREND_PERIOD



        return atr










    # =====================================================
    # SUPERTREND
    # =====================================================

    def calculate_supertrend(self):


        atr = self.calculate_atr()



        if atr is None:


            return None





        candle = self.candles[-1]



        close = float(

            candle["close"]

        )



        high = float(

            candle["high"]

        )



        low = float(

            candle["low"]

        )





        hl2 = (

            high

            +

            low

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






        if close > upper:


            return "UP"




        elif close < lower:


            return "DOWN"





        # 기존 방향 유지

        if self.last_market:


            return self.last_market.get(

                "supertrend"

            )



        return None











    # =====================================================
    # GET MARKET
    # =====================================================

    def get_market_data(
        self,
        candle=None
    ):


        return self.last_market










indicator_engine = IndicatorEngine()
