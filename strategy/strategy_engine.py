from indicators.indicator_engine import indicator_engine

from execution.execution_engine import execution_engine



class StrategyEngine:


    def __init__(self):

        self.last_signal = None

        self.last_timestamp = None


        print(
            "[STRATEGY ENGINE READY]"
        )



    # ==================================
    # CANDLE
    # ==================================

    def on_candle(
        self,
        candle
    ):


        try:


            # 완성 캔들만 처리

            if not candle.get(
                "confirm",
                False
            ):

                return None



            timestamp = int(
                candle.get(
                    "timestamp",
                    0
                )
            )



            # 중복 캔들 방지

            if timestamp == self.last_timestamp:

                return None



            self.last_timestamp = timestamp



            # ==============================
            # INDICATOR UPDATE
            # ==============================

            indicator_engine.update(
                candle
            )



            market = indicator_engine.get_market_data(
                candle
            )



            if market is None:

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
                "[INDICATOR]",
                f"PRICE={close}",
                f"VWAP={vwap}",
                f"TREND={trend}"
            )



            signal = None



            # ==============================
            # STRATEGY RULE
            # ==============================


            if close > vwap and trend == "UP":

                signal = "BUY"



            elif close < vwap and trend == "DOWN":

                signal = "SELL"




            if signal is None:

                return None




            # 같은 방향 반복 진입 방지

            if signal == self.last_signal:

                print(
                    "[SIGNAL SKIP] SAME SIGNAL",
                    signal
                )

                return None



            self.last_signal = signal



            print(
                "[TRADE SIGNAL]",
                signal
            )



            # ==============================
            # EXECUTION
            # ==============================

            result = execution_engine.execute(
                signal
            )



            return result



        except Exception as e:


            print(
                "[STRATEGY ERROR]",
                e
            )


            return None




strategy_engine = StrategyEngine()
