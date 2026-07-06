import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class PositionManager:

    def __init__(self):

        self.positions = {}
        self.realized_pnl = 0.0
        self.equity = 1000.0

    # =====================================================
    # OPEN POSITION
    # =====================================================
    def open_position(self, symbol, side, qty, price):

        self.positions[symbol] = {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "entry_price": price,
            "opened_at": datetime.utcnow(),
            "unrealized_pnl": 0.0
        }

        logger.info(f"POSITION OPENED: {symbol} {side} @ {price}")

    # =====================================================
    # CLOSE POSITION (FIXED)
    # =====================================================
    def close_position(self, symbol, price):

        pos = self.positions.get(symbol)

        if not pos:
            return None

        pnl = self.calculate_pnl(symbol, price)

        self.realized_pnl += pnl
        self.equity += pnl

        logger.info(f"POSITION CLOSED: {symbol} PnL={pnl} EQUITY={self.equity}")

        del self.positions[symbol]

        return pnl

    # =====================================================
    # PnL CALC
    # =====================================================
    def calculate_pnl(self, symbol, current_price):

        pos = self.positions.get(symbol)

        if not pos:
            return 0

        entry = pos["entry_price"]
        qty = pos["qty"]
        side = pos["side"]

        if side.upper() in ["BUY", "LONG"]:
            pnl = (current_price - entry) * qty
        else:
            pnl = (entry - current_price) * qty

        return pnl

    # =====================================================
    # UPDATE UNREALIZED PNL
    # =====================================================
    def update_unrealized(self, symbol, price):

        pos = self.positions.get(symbol)

        if not pos:
            return 0

        pnl = self.calculate_pnl(symbol, price)

        pos["unrealized_pnl"] = pnl

        return pnl

    # =====================================================
    # GETTERS
    # =====================================================
    def get_position(self, symbol):
        return self.positions.get(symbol)

    def has_position(self, symbol):
        return symbol in self.positions

    def get_equity(self):
        return self.equity


# singleton
position_manager = PositionManager()
