from strategy.indicators import indicators



class VWAPSuperTrendStrategy:


    def __init__(
        self,
        st_length=14,
        st_multiplier=3.0
    ):


        self.st_length = st_length

        self.st_multiplier = st_multiplier

        self.position = {}





    def analyze(
        self,
        candles
    ):


        if not candles:

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






        vwap = indicators.vwap(

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



        if not st:

            return None





        price = closes[-1]

        direction = st["direction"]



        current = self.position.get(
            "side"
        )





        # ====================
        # BUY
        # ====================

        if (

            direction == 1

            and

            price > vwap

            and

            current != "Buy"

        ):


            self.position["side"] = "Buy"


            return {


                "type":
                    "ENTRY",


                "side":
                    "Buy",


                "price":
                    price,


                "vwap":
                    vwap,


                "supertrend":
                    direction

            }





        # ====================
        # SELL
        # ====================

        if (

            direction == -1

            and

            price < vwap

            and

            current != "Sell"

        ):


            self.position["side"] = "Sell"


            return {


                "type":
                    "ENTRY",


                "side":
                    "Sell",


                "price":
                    price,


                "vwap":
                    vwap,


                "supertrend":
                    direction

            }





        # ====================
        # EXIT
        # ====================

        if current:


            if (

                current == "Buy"

                and

                direction == -1

            ) or (

                current == "Sell"

                and

                direction == 1

            ):


                old = current


                self.position.clear()


                return {


                    "type":
                        "EXIT",


                    "side":
                        old

                }



        return None





vwap_supertrend_strategy = VWAPSuperTrendStrategy()
