import time
import threading



class CandleBuilder:
    """
    Multi Symbol Candle Builder

    기능:
    - Tick 누적
    - 1분 OHLCV 생성
    - VWAP용 volume 저장
    """



    def __init__(
        self,
        interval=60
    ):

        self.interval = interval

        self.lock = threading.Lock()

        self.current = {}

        self.candles = {}





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


            if symbol not in self.current:


                self.current[symbol] = {

                    "symbol": symbol,

                    "timestamp": bucket,

                    "open": price,

                    "high": price,

                    "low": price,

                    "close": price,

                    "volume": volume,

                    "closed": False

                }


                return





            candle = self.current[symbol]



            # 새로운 candle 시작

            if candle["timestamp"] != bucket:


                candle["closed"] = True


                self.candles.setdefault(

                    symbol,

                    []

                ).append(

                    candle.copy()

                )



                if len(
                    self.candles[symbol]
                ) > 300:

                    self.candles[symbol].pop(0)



                self.current[symbol] = {


                    "symbol": symbol,

                    "timestamp": bucket,

                    "open": price,

                    "high": price,

                    "low": price,

                    "close": price,

                    "volume": volume,

                    "closed": False

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
    # CLOSED CHECK
    # =====================================

    def is_closed(
        self,
        symbol
    ):


        with self.lock:


            candle = self.current.get(

                symbol

            )


            if not candle:

                return False



            now = int(time.time())

            bucket = now - (

                now % self.interval

            )


            return candle["timestamp"] != bucket





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



            result = candle.copy()



            result.pop(

                "closed",

                None

            )



            return result





    # =====================================
    # GET CURRENT
    # =====================================

    def get_latest(
        self,
        symbol
    ):


        with self.lock:


            return self.current.get(

                symbol

            )





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
        symbol
    ):


        with self.lock:


            if symbol in self.current:

                del self.current[symbol]


            if symbol in self.candles:

                del self.candles[symbol]





# singleton

candle_builder = CandleBuilder()
