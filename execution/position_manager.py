import numpy as np


class PositionManager:

    # =========================
    # ATR 기반 TP/SL 계산
    # =========================
    def calc_atr_levels(self, prices, multiplier=2.0):

        if len(prices) < 20:
            return None, None

        high = max(prices[-20:])
        low = min(prices[-20:])
        atr = (high - low) / 20

        tp = atr * multiplier
        sl = atr * multiplier

        return tp, sl

    # =========================
    # 손절 체크
    # =========================
    def should_stop_loss(self, entry_price, current_price, side, sl):

        if side == "Buy":
            return current_price <= entry_price - sl

        if side == "Sell":
            return current_price >= entry_price + sl

        return False

    # =========================
    # 익절 체크
    # =========================
    def should_take_profit(self, entry_price, current_price, side, tp):

        if side == "Buy":
            return current_price >= entry_price + tp

        if side == "Sell":
            return current_price <= entry_price - tp

        return False

    # =========================
    # 자동 청산 판단
    # =========================
    def evaluate_exit(self, symbol, entry_price, side, prices):

        current_price = prices[-1]

        tp, sl = self.calc_atr_levels(prices)

        if tp is None:
            return None

        if self.should_stop_loss(entry_price, current_price, side, sl):
            return "STOP_LOSS"

        if self.should_take_profit(entry_price, current_price, side, tp):
            return "TAKE_PROFIT"

        return None
