from config import DEFAULT_SYMBOL


class StrategyEngine:

    def __init__(self):
        self.last_signal = None

        print("==============================")
        print("[STRATEGY ENGINE READY]")
        print("==============================")


    def on_candle(self, candle, indicator):

        price = candle["close"]

        vwap = indicator.get("vwap")
        trend = indicator.get("trend")


        signal = "HOLD"


        # BUY 조건
        if trend is True and price > vwap:
            signal = "BUY"


        # SELL 조건
        elif trend is False and price < vwap:
            signal = "SELL"



        if signal != self.last_signal:

            print("==============================")
            print("[SIGNAL]")
            print("SYMBOL :", DEFAULT_SYMBOL)
            print("PRICE  :", price)
            print("VWAP   :", vwap)
            print("TREND  :", trend)
            print("ACTION :", signal)
            print("==============================")


            self.last_signal = signal


        return signal



strategy_engine = StrategyEngine()
