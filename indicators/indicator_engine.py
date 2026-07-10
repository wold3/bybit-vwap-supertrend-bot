# =====================================================
# indicators/indicator_engine.py
# VWAP + SuperTrend Indicator Engine
# =====================================================

from collections import deque


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


        self.last_supertrend = None



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





        self.last_supertrend = trend



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


            high = float(

                c["high"]

            )


            low = float(

                c["low"]

            )


            close = float(

                c["close"]

            )



            volume = float(

                c["volume"]

            )



            typical_price = (

                high

                +

                low

                +

                close

            ) / 3




            total_value += (

                typical_price

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



        if len(data) < SUPERTREND_PERIOD + 1:


            return None





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


                abs(

                    high - prev_close

                ),


                abs(

                    low - prev_close

                )

            )



            trs.append(

                tr

            )







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






        upper_band = (

            hl2

            +

            SUPERTREND_MULTIPLIER

            *

            atr

        )





        lower_band = (

            hl2

            -

            SUPERTREND_MULTIPLIER

            *

            atr

        )








        previous = self.last_supertrend





        # ==============================
        # TREND CONTINUATION
        # ==============================


        if previous == "UP":


            if close < lower_band:

                return "DOWN"


            return "UP"





        if previous == "DOWN":


            if close > upper_band:

                return "UP"


            return "DOWN"







        # ==============================
        # FIRST TREND
        # ==============================


        if close > upper_band:


            return "UP"




        if close < lower_band:


            return "DOWN"





        return "UP"







    # =====================================================
    # GET MARKET
    # =====================================================

    def get_market_data(
        self,
        candle=None
    ):


        return self.last_market







# =====================================================
# SINGLETON
# =====================================================

indicator_engine = IndicatorEngine()
