import time
from collections import deque


class CandleBuilder:

    def __init__(self, interval=60):
        self.interval = interval  # 1분 캔들
        self.current_candle = None
        self.candles = deque(maxlen=200)

    def update(self, price):

        now = int(time.time())

        bucket = now - (now % self.interval)

        # 새 캔들 시작
        if self.current_candle is None or self.current_candle["time"] != bucket:

            if self.current_candle:
                self.candles.append(self.current_candle)

            self.current_candle = {
                "time": bucket,
                "open": price,
                "high": price,
                "low": price,
                "close": price
            }

        # 기존 캔들 업데이트
        else:
            c = self.current_candle
            c["high"] = max(c["high"], price)
            c["low"] = min(c["low"], price)
            c["close"] = price

    def get_candles(self):
        return list(self.candles)

    def get_current(self):
        return self.current_candle


candle_builder = CandleBuilder()
