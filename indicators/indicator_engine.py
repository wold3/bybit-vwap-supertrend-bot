import collections
import math



class IndicatorEngine:


    def __init__(self):


        self.max_history = 200


        self.candles = collections.deque(
            maxlen=self.max_history
        )


        self.vwap = None

        self.supertrend = None


        self.last_close = None



        # Supertrend 설정

        self.atr_period = 10

        self.multiplier = 3



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


            if not candle.get(
                "confirm",
                False
            ):

                return None



            self.candles.append(
                candle
            )



            if len(self.candles) < self.atr_period + 2:

                return None



            self.calculate_vwap()


            self.calculate_supertrend()



            self.last_close = float(
                candle["close"]
            )



            return True



        except Exception as e:


            print(
                "[INDICATOR UPDATE ERROR]",
                e
            )


            return None





    # =====================================================
    # VWAP
    # =====================================================

    def calculate_vwap(self):


        try:


            total_volume = 0

            total_price_volume = 0



            for c in self.candles:


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



                total_price_volume += (
                    typical_price
                    *
                    volume
                )


                total_volume += volume



            if total_volume > 0:


                self.vwap = (
                    total_price_volume
                    /
                    total_volume
                )



        except Exception as e:


            print(
                "[VWAP ERROR]",
                e
            )






    # =====================================================
    # ATR
    # =====================================================

    def calculate_atr(self):


        trs = []



        candles = list(
            self.candles
        )



        for i in range(
            1,
            len(candles)
        ):


            current = candles[i]

            previous = candles[i-1]



            high = float(
                current["high"]
            )

            low = float(
                current["low"]
            )

            prev_close = float(
                previous["close"]
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



        if len(trs) < self.atr_period:


            return None



        recent = trs[
            -self.atr_period:
        ]



        return sum(recent) / self.atr_period







    # =====================================================
    # SUPERTREND
    # =====================================================

    def calculate_supertrend(self):


        try:


            atr = self.calculate_atr()



            if atr is None:

                return None




            candle = self.candles[-1]



            high = float(
                candle["high"]
            )


            low = float(
                candle["low"]
            )


            close = float(
                candle["close"]
            )



            middle = (
                high
                +
                low
            ) / 2




            upper = (
                middle
                +
                self.multiplier
                *
                atr
            )



            lower = (
                middle
                -
                self.multiplier
                *
                atr
            )



            if close > upper:


                self.supertrend = "UP"



            elif close < lower:


                self.supertrend = "DOWN"



            else:


                if self.supertrend is None:

                    self.supertrend = "UP"




        except Exception as e:


            print(
                "[SUPERTREND ERROR]",
                e
            )







    # =====================================================
    # MARKET DATA
    # =====================================================

    def get_market_data(
        self,
        candle=None
    ):


        if self.vwap is None:

            return None



        if self.supertrend is None:

            return None



        return {


            "vwap":

                round(
                    self.vwap,
                    4
                ),



            "supertrend":

                self.supertrend,



            "close":

                float(
                    candle["close"]
                )
                if candle
                else self.last_close,



            "count":

                len(
                    self.candles
                )

        }






indicator_engine = IndicatorEngine()
