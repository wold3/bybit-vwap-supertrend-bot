from strategy.indicators import indicators


class VWAPSuperTrendStrategy:


    def __init__(
        self,
        st_length=10,
        st_multiplier=3.0,
        volume_multiplier=1.2
    ):

        self.st_length = st_length

        self.st_multiplier = st_multiplier

        self.volume_multiplier = volume_multiplier

        self.previous_direction = None



    # =====================================================
    # ANALYZE
    # =====================================================

    def analyze(
        self,
        candles,
        current_position=None
    ):


        if not candles:

            return None



        if len(candles) < self.st_length + 5:

            return None



        highs = [

            float(c["high"])

            for c in candles

        ]


        lows = [

            float(c["low"])

            for c in candles

        ]


        closes = [

            float(c["close"])

            for c in candles

        ]


        volumes = [

            float(c["volume"])

            for c in candles

        ]



        # =================================================
        # INDICATORS
        # =================================================


        vwap = indicators.vwap(

            highs,
            lows,
            closes,
            volumes

        )



        st = indicators.supertrend(

            highs,
            lows,
            closes,

            self.st_length,

            self.st_multiplier

        )



        if st is None:

            return None



        price = closes[-1]


        direction = st["direction"]



        # =================================================
        # SUPERTREND FLIP CHECK
        # =================================================


        changed = False


        if self.previous_direction is not None:


            if direction != self.previous_direction:

                changed = True



        self.previous_direction = direction



        if not changed:

            return None



        # =================================================
        # VOLUME FILTER
        # =================================================


        avg_volume = sum(

            volumes[-20:]

        ) / min(

            20,
            len(volumes)

        )


        volume_ok = (

            volumes[-1]

            >=

            avg_volume

            *

            self.volume_multiplier

        )



        if not volume_ok:

            return None



        # =================================================
        # LONG ENTRY
        # =================================================


        if (

            direction == 1

            and

            price > vwap

            and

            current_position != "Buy"

        ):


            return {


                "type":

                    "ENTRY",


                "side":

                    "Buy",


                "price":

                    price,


                "vwap":

                    vwap,


                "atr":

                    st["atr"],


                "supertrend":

                    direction,


                "reason":

                    "SUPERTREND_FLIP_UP"

            }



        # =================================================
        # SHORT ENTRY
        # =================================================


        if (

            direction == -1

            and

            price < vwap

            and

            current_position != "Sell"

        ):


            return {


                "type":

                    "ENTRY",


                "side":

                    "Sell",


                "price":

                    price,


                "vwap":

                    vwap,


                "atr":

                    st["atr"],


                "supertrend":

                    direction,


                "reason":

                    "SUPERTREND_FLIP_DOWN"

            }



        # =================================================
        # EXIT
        # =================================================


        if current_position:


            if (

                current_position == "Buy"

                and

                direction == -1

            ):


                return {


                    "type":

                        "EXIT",


                    "side":

                        "Buy",


                    "reason":

                        "SUPERTREND_REVERSAL"

                }



            if (

                current_position == "Sell"

                and

                direction == 1

            ):


                return {


                    "type":

                        "EXIT",


                    "side":

                        "Sell",


                    "reason":

                        "SUPERTREND_REVERSAL"

                }



        return None



# singleton

vwap_supertrend_strategy = VWAPSuperTrendStrategy()
