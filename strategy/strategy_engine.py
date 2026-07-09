from indicators.indicator_engine import indicator_engine


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



            # 동일 캔들 중복 방지

            if timestamp == self.last_timestamp:

                return None



            self.last_timestamp = timestamp



            # ==================================
            # INDICATOR UPDATE
            # ==================================

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



            # ==================================
            # STRATEGY RULE
            # ==================================

            if close > vwap and trend == "UP":

                signal = "BUY"



            elif close < vwap and trend == "DOWN":

                signal = "SELL"



            else:

                signal = None



            if signal is None:

                return None



            # ==================================
            # DUPLICATE SIGNAL FILTER
            # ==================================

            if signal == self.last_signal:

                print(
                    "[SIGNAL SKIP]",
                    signal
                )

                return None



            self.last_signal = signal



            print(
                "[TRADE SIGNAL]",
                signal
            )



            # main.py에서 실행 처리
            return signal



        except Exception as e:


            print(
                "[STRATEGY ERROR]",
                e
            )


            return None




strategy_engine = StrategyEngine()
