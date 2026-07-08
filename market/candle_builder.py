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



        key = symbol



        # 새 캔들 시작

        if key not in self.current:


            self.current[key] = {


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




        candle = self.current[key]



        # 시간이 넘어가면 저장

        if candle_time > candle["timestamp"]:


            self.candles[key].append(

                candle.copy()

            )



            self.current[key] = {


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


        return list(

            self.candles.get(

                symbol,

                []

            )

        )





    # =====================================
    # STATUS
    # =====================================

    def status(self):


        return {


            "symbols":

                list(
                    self.candles.keys()
                ),


            "count":

                sum(

                    len(v)

                    for v in self.candles.values()

                )

        }





candle_builder = CandleBuilder()
