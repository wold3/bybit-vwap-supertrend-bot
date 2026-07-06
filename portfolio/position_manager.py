import logging

logger = logging.getLogger(__name__)


class PositionManager:

    def __init__(self):

        self.position = None

    # =====================================================
    # 포지션 오픈
    # =====================================================
    def open_position(self, symbol, side, qty, price):

        self.position = {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "entry_price": price,
            "unrealized_pnl": 0
        }

        logger.info(f"POSITION OPENED: {side} {qty} @ {price}")

    # =====================================================
    # PnL 계산
    # =====================================================
    def update_pnl(self, price):

        if not self.position:
            return 0

        entry = self.position["entry_price"]
        qty = self.position["qty"]
        side = self.position["side"]

        if side.lower() == "buy":
            pnl = (price - entry) * qty
        else:
            pnl = (entry - price) * qty

        self.position["unrealized_pnl"] = pnl

        return pnl

    # =====================================================
    # 포지션 종료
    # =====================================================
    def close_position(self):

        if not self.position:
            return 0

        pnl = self.position["unrealized_pnl"]

        logger.info(f"POSITION CLOSED PNL={pnl}")

        self.position = None

        return pnl


position_manager = PositionManager()
