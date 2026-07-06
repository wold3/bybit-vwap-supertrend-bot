import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class PositionManager:

    def __init__(self):

        # symbol -> position
        self.positions = {}

    # =====================================================
    # 포지션 오픈
    # =====================================================
    def open_position(self, symbol, side, qty, price):

        self.positions[symbol] = {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "entry_price": price,
            "opened_at": datetime.utcnow()
        }

        logger.info(f"POSITION OPENED: {symbol} {side} @ {price}")

    # =====================================================
    # 포지션 종료
    # =====================================================
    def close_position(self, symbol, price):

        pos = self.positions.get(symbol)

        if not pos:
            return None

        pnl = self.calculate_pnl(symbol, price)

        logger.info(f"POSITION CLOSED: {symbol} PnL={pnl}")

        del self.positions[symbol]

        return pnl

    # =====================================================
    # PnL 계산
    # =====================================================
    def calculate_pnl(self, symbol, current_price):

        pos = self.positions.get(symbol)

        if not pos:
            return 0

        entry = pos["entry_price"]
        qty = pos["qty"]
        side = pos["side"]

        if side.upper() == "BUY":
            pnl = (current_price - entry) * qty
        else:
            pnl = (entry - current_price) * qty

        return pnl

    # =====================================================
    # 상태 조회
    # =====================================================
    def get_position(self, symbol):

        return self.positions.get(symbol)

    def has_position(self, symbol):

        return symbol in self.positions


# singleton
position_manager = PositionManager()
