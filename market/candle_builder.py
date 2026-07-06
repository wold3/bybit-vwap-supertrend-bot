import time
from collections import deque


class CandleBuilder:

    def __init__(self, interval=60):
        self.interval = interval
        self.current = None
        self.candles = deque(maxlen=300)

    def update(self, price):

        now = int(time.time())
        bucket = now - (now % self.interval)

        if self.current is None or self.current["time"] != bucket:

            if self.current:
                self.candles.append(self.current)

            self.current = {
                "time": bucket,
                "open": price,
                "high": price,
                "low": price,
                "close": price
            }

        else:
            c = self.current
            c["high"] = max(c["high"], price)
            c["low"] = min(c["low"], price)
            c["close"] = price

    def get_candles(self):
        return list(self.candles)


candle_builder = CandleBuilder()
