import time
from collections import defaultdict, deque



class CandleBuilder:


    def __init__(
        self,
        interval=60
    ):


        self.interval = interval


        self.current = {}


        self.candles = defaultdict(

            lambda: deque(maxlen=300)

        )





    # =====================================
    # UPDATE TICK
    # =====================================

    def update(
        self,
        symbol,
        price,
        volume
    ):


        now = int(

            time.time()

        )


        bucket = now - (

            now % self.interval

        )



        candle = self.current.get(

            symbol

        )



        # 새로운 candle

        if candle is None or candle["timestamp"] != bucket:



            if candle:


                self.candles[symbol].append(

                    candle

                )



            self.current[symbol] = {


                "symbol":

                    symbol,


                "open":

                    float(price),


                "high":

                    float(price),


                "low":

                    float(price),


                "close":

                    float(price),


                "volume":

                    float(volume),


                "timestamp":

                    bucket


            }



            return None





        # 기존 candle 업데이트


        candle["high"] = max(

            candle["high"],

            float(price)

        )


        candle["low"] = min(

            candle["low"],

            float(price)

        )


        candle["close"] = float(price)



        candle["volume"] += float(volume)





    # =====================================
    # CLOSE CURRENT CANDLE
    # =====================================

    def close_candle(
        self,
        symbol
    ):


        candle = self.current.get(

            symbol

        )



        if not candle:


            return None



        self.candles[symbol].append(

            candle.copy()

        )



        del self.current[symbol]



        return candle





    # =====================================
    # LATEST CLOSED CANDLE
    # =====================================

    def get_latest(
        self,
        symbol
    ):


        if not self.candles[symbol]:

            return None



        return self.candles[symbol][-1]





    # =====================================
    # ALL CANDLES
    # =====================================

    def get_candles(
        self,
        symbol
    ):


        return list(

            self.candles[symbol]

        )





    # =====================================
    # RESET
    # =====================================

    def reset(
        self,
        symbol=None
    ):


        if symbol:


            self.current.pop(

                symbol,

                None

            )


            self.candles[symbol].clear()



        else:


            self.current.clear()


            self.candles.clear()





# singleton

candle_builder = CandleBuilder()
