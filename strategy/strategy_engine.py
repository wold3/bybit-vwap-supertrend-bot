import time


from indicators.indicator_engine import (
    indicator_engine
)


from config import (
    DEFAULT_SYMBOL,
)



class StrategyEngine:


    def __init__(self):


        self.symbol = DEFAULT_SYMBOL


        self.last_timestamp = None

        self.last_signal = None


        print("==============================")
        print("[STRATEGY ENGINE READY]")
        print("SYMBOL :", self.symbol)
        print("==============================")




    # =====================================================
    # CANDLE PROCESS
    # =====================================================

    def on_candle(
        self,
        candle
    ):


        try:


            # -----------------------------
            # CONFIRM CHECK
            # -----------------------------

            if not candle.get(
                "confirm",
                False
            ):

                return None




            timestamp = int(
                candle["timestamp"]
            )



            # -----------------------------
            # DUPLICATE CANDLE
            # -----------------------------

            if timestamp == self.last_timestamp:

                return None



            self.last_timestamp = timestamp





            # -----------------------------
            # UPDATE INDICATOR
            # -----------------------------

            indicator_engine.update(
                candle
            )



            market = (

                indicator_engine
                .get_market_data(
                    candle
                )

            )



            if market is None:

                print(
                    "[STRATEGY WAIT] INDICATOR"
                )

                return None





            close = float(
                candle["close"]
            )


            vwap = market.get(
                "vwap"
            )


            trend = market.get(
                "supertrend"
            )



            if vwap is None:

                return None


            if trend is None:

                return None





            print(
                "[MARKET]",
                "PRICE:",
                close,
                "VWAP:",
                round(vwap,2),
                "TREND:",
                trend
            )





            signal = None





            # =================================================
            # ENTRY RULE
            # =================================================


            # LONG

            if (

                close > vwap

                and

                trend == "UP"

            ):

                signal = "BUY"




            # SHORT

            elif (

                close < vwap

                and

                trend == "DOWN"

            ):

                signal = "SELL"






            if signal is None:

                return None





            # =================================================
            # DUPLICATE SIGNAL BLOCK
            # =================================================


            if signal == self.last_signal:


                print(
                    "[SIGNAL BLOCK] SAME SIGNAL",
                    signal
                )


                return None




            self.last_signal = signal




            print(
                "=============================="
            )

            print(
                "[TRADE SIGNAL]",
                signal
            )

            print(
                "=============================="
            )



            return signal






        except Exception as e:


            print(
                "[STRATEGY ERROR]",
                e
            )


            return None






    # =====================================================
    # RESET
    # =====================================================

    def reset(self):


        self.last_timestamp = None

        self.last_signal = None


        print(
            "[STRATEGY RESET]"
        )







strategy_engine = StrategyEngine()
