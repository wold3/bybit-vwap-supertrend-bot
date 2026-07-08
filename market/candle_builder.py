import os
import time
from collections import defaultdict, deque

from dotenv import load_dotenv


load_dotenv()


class CandleBuilder:


    def __init__(self):


        self.interval = int(
            os.getenv(
                "CANDLE_INTERVAL",
                "60"
            )
        )


        self.max_history = int(
            os.getenv(
                "MAX_HISTORY",
                "500"
            )
        )


        self.candles = defaultdict(
            lambda:
                deque(
                    maxlen=self.max_history
                )
        )


        # 현재 진행중 캔들
        self.current = {}




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


        candle_time = now - (
            now % self.interval
        )



        # 첫 tick
        if symbol not in self.current:


            self.current[symbol] = {


                "symbol":
                    symbol,


                "timestamp":
                    candle_time,


                "open":
                    price,


                "high":
                    price,


                "low":
                    price,


                "close":
                    price,


                "volume":
                    volume

            }


            return




        candle = self.current[symbol]



        # =====================================
        # 새 캔들 생성
        # =====================================

        if candle_time > candle["timestamp"]:



            # 이전 캔들 저장

            self.candles[symbol].append(

                candle.copy()

            )



            # 새 캔들 시작

            self.current[symbol] = {


                "symbol":
                    symbol,


                "timestamp":
                    candle_time,


                "open":
                    price,


                "high":
                    price,


                "low":
                    price,


                "close":
                    price,


                "volume":
                    volume

            }



        else:



            # 현재 캔들 업데이트

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
    # GET CANDLES
    # =====================================

    def get_candles(
        self,
        symbol
    ):


        result = list(

            self.candles.get(

                symbol,

                []

            )

        )


        # 진행중 캔들 포함

        if symbol in self.current:


            result.append(

                self.current[symbol].copy()

            )


        return result





    # =====================================
    # GET CURRENT
    # =====================================

    def get_current(
        self,
        symbol
    ):


        return self.current.get(

            symbol

        )





    # =====================================
    # RESET
    # =====================================

    def reset(
        self,
        symbol=None
    ):


        if symbol:


            self.candles.pop(

                symbol,

                None

            )


            self.current.pop(

                symbol,

                None

            )


        else:


            self.candles.clear()

            self.current.clear()





    # =====================================
    # STATUS
    # =====================================

    def status(self):


        return {


            "symbols":

                list(

                    self.candles.keys()

                ),


            "history_count":

                sum(

                    len(v)

                    for v in self.candles.values()

                ),


            "current":

                list(

                    self.current.keys()

                ),


            "interval":

                self.interval

        }





candle_builder = CandleBuilder()
