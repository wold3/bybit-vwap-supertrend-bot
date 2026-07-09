import os
from collections import defaultdict, deque

import pandas as pd
from dotenv import load_dotenv


load_dotenv()


class IndicatorEngine:

    def __init__(self):

        self.max_history = int(
            os.getenv(
                "MAX_HISTORY",
                "500"
            )
        )

        self.period = int(
            os.getenv(
                "SUPER_TREND_PERIOD",
                "10"
            )
        )

        self.multiplier = float(
            os.getenv(
                "SUPER_TREND_MULTIPLIER",
                "3.0"
            )
        )

        self.history = defaultdict(
            lambda: deque(
                maxlen=self.max_history
            )
        )

        print("[INDICATOR ENGINE READY]")


    # =====================================
    # UPDATE CANDLE
    # =====================================

    def update(self, candle):

        if not candle:
            return


        symbol = candle.get("symbol")

        if not symbol:
            return


        normalized = {

            "symbol": symbol,

            "timestamp": int(
                candle.get(
                    "timestamp",
                    0
                )
            ),

            "open": float(
                candle.get(
                    "open",
                    0
                )
            ),

            "high": float(
                candle.get(
                    "high",
                    0
                )
            ),

            "low": float(
                candle.get(
                    "low",
                    0
                )
            ),

            "close": float(
                candle.get(
                    "close",
                    0
                )
            ),

            "volume": float(
                candle.get(
                    "volume",
                    0
                )
            ),

            "confirm": candle.get(
                "confirm",
                False
            )

        }


        self.history[symbol].append(
            normalized
        )


    # =====================================
    # DATAFRAME
    # =====================================

    def dataframe(self, symbol):

        data = self.history.get(
            symbol
        )


        if not data:

            return None


        return pd.DataFrame(
            list(data)
        )


    # =====================================
    # VWAP
    # =====================================

    def calculate_vwap(self, symbol):

        df = self.dataframe(
            symbol
        )


        if df is None or len(df) == 0:

            return None


        typical_price = (

            df["high"]

            +

            df["low"]

            +

            df["close"]

        ) / 3


        volume = df["volume"]


        total_volume = volume.sum()


        if total_volume <= 0:

            return None


        return float(

            (
                typical_price * volume
            ).sum()

            /

            total_volume

        )


    # =====================================
    # ATR
    # =====================================

    def calculate_atr(self, symbol):

        df = self.dataframe(
            symbol
        )


        if df is None:

            return None


        if len(df) < self.period:

            return None


        high = df["high"]

        low = df["low"]

        close = df["close"]


        tr1 = high - low

        tr2 = (
            high - close.shift()
        ).abs()

        tr3 = (
            low - close.shift()
        ).abs()


        tr = pd.concat(
            [
                tr1,
                tr2,
                tr3
            ],
            axis=1
        ).max(axis=1)


        atr = tr.rolling(
            self.period
        ).mean()


        value = atr.iloc[-1]


        if pd.isna(value):

            return None


        return float(value)


    # =====================================
    # SUPER TREND
    # =====================================

    def calculate_supertrend(self, symbol):

        df = self.dataframe(
            symbol
        )


        if df is None:

            return "FLAT"


        atr = self.calculate_atr(
            symbol
        )


        if atr is None:

            return "FLAT"


        current = df.iloc[-1]


        hl2 = (

            current["high"]

            +

            current["low"]

        ) / 2


        upper_band = (
            hl2
            +
            self.multiplier * atr
        )


        lower_band = (
            hl2
            -
            self.multiplier * atr
        )


        close = current["close"]


        if close > upper_band:

            return "UP"


        elif close < lower_band:

            return "DOWN"


        return "FLAT"


    # =====================================
    # CALCULATE ALL
    # =====================================

    def calculate(self, symbol):

        return {

            "vwap":
                self.calculate_vwap(
                    symbol
                ),


            "supertrend":
                self.calculate_supertrend(
                    symbol
                )

        }


    # =====================================
    # MARKET DATA
    # =====================================

    def get_market_data(self, candle):

        if not candle:

            return None


        symbol = candle.get(
            "symbol"
        )


        if not symbol:

            return None


        indicators = self.calculate(
            symbol
        )


        return {

            **candle,

            **indicators

        }


    # =====================================
    # RESET
    # =====================================

    def reset(self, symbol=None):

        if symbol:

            self.history.pop(
                symbol,
                None
            )

        else:

            self.history.clear()


    # =====================================
    # STATUS
    # =====================================

    def status(self):

        return {

            "symbols":
                list(
                    self.history.keys()
                ),

            "count":
                sum(
                    len(v)
                    for v in self.history.values()
                ),

            "period":
                self.period,

            "multiplier":
                self.multiplier

        }



indicator_engine = IndicatorEngine()
