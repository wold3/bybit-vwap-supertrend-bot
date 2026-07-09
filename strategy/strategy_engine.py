from indicators.vwap import calculate_vwap
from indicators.supertrend import supertrend


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

            # --------------------------
            # 완성된 캔들만 사용
            # --------------------------

            if not candle.get("confirm", False):
                return None

            timestamp = int(candle["timestamp"])

            # 이미 처리한 봉이면 무시
            if timestamp == self.last_timestamp:
                return None

            self.last_timestamp = timestamp

            close = float(candle["close"])
            high = float(candle["high"])
            low = float(candle["low"])

            # --------------------------
            # Indicator
            # --------------------------

            vwap = calculate_vwap(candle)

            trend = supertrend.update(
                high,
                low,
                close
            )

            print(
                "[INDICATOR]",
                f"PRICE={close}",
                f"VWAP={vwap}",
                f"TREND={trend}"
            )

            # --------------------------
            # Signal
            # --------------------------

            signal = None

            if close > vwap and trend:
                signal = "BUY"

            elif close < vwap and not trend:
                signal = "SELL"

            # --------------------------
            # HOLD
            # --------------------------

            if signal is None:
                return None

            # --------------------------
            # 같은 신호 반복 방지
            # --------------------------

            if signal == self.last_signal:
                return None

            self.last_signal = signal

            print("[TRADE SIGNAL]", signal)

            return signal

        except Exception as e:

            print("[STRATEGY ERROR]", e)

            return None


strategy_engine = StrategyEngine()
