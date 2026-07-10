from config import (
    DEFAULT_SYMBOL,
)



class StrategyEngine:


    def __init__(self):


        self.symbol = DEFAULT_SYMBOL


        self.last_signal = "HOLD"


        print("==============================")
        print("[STRATEGY ENGINE READY]")
        print("==============================")









    # =====================================================
    # ANALYZE
    # =====================================================

    def analyze(
        self,
        candle,
        indicators
    ):


        try:


            if not indicators:


                return "HOLD"






            vwap = indicators.get(
                "vwap"
            )


            trend = indicators.get(
                "supertrend"
            )






            if vwap is None:


                return "HOLD"








            close = float(

                candle["close"]

            )







            signal = "HOLD"








            # =========================
            # BUY
            # =========================

            if (

                close > vwap

                and

                trend == "UP"

            ):


                signal = "BUY"







            # =========================
            # SELL
            # =========================

            elif (

                close < vwap

                and

                trend == "DOWN"

            ):


                signal = "SELL"








            if signal != self.last_signal:


                print(
                    "[STRATEGY SIGNAL]",
                    signal,
                    "| PRICE:",
                    close,
                    "| VWAP:",
                    vwap,
                    "| TREND:",
                    trend
                )



            self.last_signal = signal



            return signal








        except Exception as e:


            print(
                "[STRATEGY ERROR]",
                e
            )


            return "HOLD"









    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "symbol":

                self.symbol,


            "last_signal":

                self.last_signal,


        }











strategy_engine = StrategyEngine()
