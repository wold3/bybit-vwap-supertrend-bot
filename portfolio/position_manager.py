import time


class PositionManager:

    def __init__(self):

        # symbol 기준 포지션 저장
        self.positions = {}

    # =================================================
    # 포지션 오픈
    # =================================================
    def open_position(self, symbol, side, qty, entry_price):

        self.positions[symbol] = {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "entry_price": entry_price,
            "open_time": time.time(),
            "unrealized_pnl": 0.0
        }

    # =================================================
    # 포지션 업데이트 (PnL 계산)
    # =================================================
    def update_price(self, symbol, current_price):

        if symbol not in self.positions:
            return None

        pos = self.positions[symbol]

        entry = pos["entry_price"]
        qty = pos["qty"]

        if pos["side"] == "BUY":
            pnl = (current_price - entry) * qty
        else:
            pnl = (entry - current_price) * qty

        pos["unrealized_pnl"] = pnl

        return pnl

    # =================================================
    # 손절 / 익절 체크
    # =================================================
    def check_exit(self, symbol, sl_pct=-0.5, tp_pct=1.0):

        if symbol not in self.positions:
            return None

        pos = self.positions[symbol]

        entry = pos["entry_price"]
        pnl_pct = (pos["unrealized_pnl"] / entry) * 100

        # 손절
        if pnl_pct <= sl_pct:
            return "STOP_LOSS"

        # 익절
        if pnl_pct >= tp_pct:
            return "TAKE_PROFIT"

        return None

    # =================================================
    # 포지션 종료
    # =================================================
    def close_position(self, symbol):

        if symbol in self.positions:
            del self.positions[symbol]

    # =================================================
    # 현재 포지션 조회
    # =================================================
    def get_position(self, symbol):

        return self.positions.get(symbol, None)


# 싱글톤
position_manager = PositionManager()
