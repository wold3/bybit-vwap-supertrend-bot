from strategy.indicators import indicators


class VWAPSuperTrendStrategy:


    def __init__(
        self,
        st_length=400,
        st_multiplier=15.0
    ):

        self.st_length = st_length
        self.st_multiplier = st_multiplier

        self.position = {}



    # =====================================
    # PROCESS CANDLES
    # =====================================

    def analyze(
        self,
        candles
    ):


        if candles is None:
            return None


        if len(candles) < self.st_length:

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
        # VWAP
        # ==========================

        vwap = indicators.vwap(

            closes,

            volumes

        )



        # ==========================
        # SuperTrend
        # ==========================

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



        signal = None



        # ==========================
        # ENTRY LOGIC
        # ==========================

        if direction == 1 and price > vwap:


            if self.position.get(
                "side"
            ) != "Buy":


                self.position["side"] = "Buy"


                signal = {

                    "type":
                        "ENTRY",

                    "side":
                        "Buy",

                    "price":
                        price

                }



        elif direction == -1 and price < vwap:


            if self.position.get(
                "side"
            ) != "Sell":


                self.position["side"] = "Sell"


                signal = {

                    "type":
                        "ENTRY",

                    "side":
                        "Sell",

                    "price":
                        price

                }



        # ==========================
        # EXIT LOGIC
        # ==========================

        elif direction == 0:


            if self.position.get("side"):

                signal = {

                    "type":
                        "EXIT",

                    "side":
                        self.position["side"]

                }


                self.position.clear()



        return signal





# singleton

vwap_supertrend_strategy = VWAPSuperTrendStrategy()
