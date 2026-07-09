from indicators.indicator_engine import indicator_engine


class StrategyEngine:

    def __init__(self):

        self.last_signal = None
        self.last_timestamp = None

        print("[STRATEGY ENGINE READY]")


    # ==================================
    # CANDLE
    # ==================================

    def on_candle(self, candle):

        try:

            # 완성 캔들만 처리
            if not candle.get("confirm", False):
                return None


            timestamp = int(candle["timestamp"])


            # 중복 캔들 방지
            if timestamp == self.last_timestamp:
                return None


            self.last_timestamp = timestamp


            # Indicator 업데이트
            indicator_engine.update(candle)


            market = indicator_engine.get_market_data(candle)


            if market is None:
                return None


            close = float(candle["close"])

            vwap = market.get("vwap")
            trend = market.get("supertrend")


            if vwap is None or trend is None:
                return None


            print(
                "[INDICATOR]",
                f"PRICE={close}",
                f"VWAP={vwap}",
                f"TREND={trend}"
            )


            signal = None


            # ==============================
            # ENTRY RULE
            # ==============================

            if close > vwap and trend == "UP":

                signal = "BUY"


            elif close < vwap and trend == "DOWN":

                signal = "SELL"



            if signal is None:

                return None



            # 동일 신호 반복 방지

            if signal == self.last_signal:

                return None



            self.last_signal = signal


            print(
                "[TRADE SIGNAL]",
                signal
            )


            return signal



        except Exception as e:

            print(
                "[STRATEGY ERROR]",
                e
            )

            return None



strategy_engine = StrategyEngine()
