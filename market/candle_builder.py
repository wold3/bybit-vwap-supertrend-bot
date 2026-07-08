# market/candle_builder.py

import time
from collections import deque
import threading



class CandleBuilder:
    """
    1분 Candle Builder

    입력:
        symbol
        price
        volume

    출력:
        OHLCV Candle
    """



    def __init__(
        self,
        interval=60
    ):


        self.interval = interval


        self.current = {}


        self.candles = {}


        self.lock = threading.Lock()





    # =====================================
    # UPDATE TICK
    # =====================================

    def update(
        self,
        symbol,
        price,
        volume
    ):


        now = int(time.time())


        bucket = now - (

            now % self.interval

        )



        with self.lock:



            candle = self.current.get(

                symbol

            )



            # 새 Candle 시작

            if candle is None or candle["timestamp"] != bucket:



                if candle:


                    self.candles.setdefault(

                        symbol,

                        deque(maxlen=300)

                    ).append(

                        candle

                    )



                self.current[symbol] = {


                    "symbol":

                        symbol,


                    "open":

                        price,


                    "high":

                        price,


                    "low":

                        price,


                    "close":

                        price,


                    "volume":

                        volume,


                    "timestamp":

                        bucket

                }



            else:



                candle["high"] = max(

                    candle["high"],

                    price

                )


                candle["low"] = min(

                    candle["low"],

                    price

                )


                candle["close"] = price


                candle["volume"] += volume





    # =====================================
    # CLOSE CANDLE
    # =====================================

    def close_candle(
        self,
        symbol
    ):


        with self.lock:


            candle = self.current.get(

                symbol

            )



            if not candle:


                return None



            return candle.copy()





    # =====================================
    # LATEST CLOSED CANDLE
    # =====================================

    def get_latest(
        self,
        symbol
    ):


        with self.lock:


            data = self.candles.get(

                symbol

            )



            if not data:


                return None



            return data[-1]





    # =====================================
    # HISTORY
    # =====================================

    def get_candles(
        self,
        symbol
    ):


        with self.lock:


            return list(

                self.candles.get(

                    symbol,

                    []

                )

            )





    # =====================================
    # RESET
    # =====================================

    def reset(
        self,
        symbol=None
    ):


        with self.lock:


            if symbol:


                self.current.pop(

                    symbol,

                    None

                )


                self.candles.pop(

                    symbol,

                    None

                )


            else:


                self.current.clear()


                self.candles.clear()





    # =====================================
    # STATUS
    # =====================================

    def status(self):


        with self.lock:


            return {


                "symbols":

                    list(

                        self.current.keys()

                    ),


                "count":

                    len(

                        self.current

                    )

            }





candle_builder = CandleBuilder()
