import logging
from datetime import datetime

from api.bybit_api import (
    close_position,
    get_position,
    get_unrealized_pnl,
    get_last_price,
)

from database.repository import (
    save_position,
    delete_position,
    update_position_price,
)

logger = logging.getLogger(__name__)


class PositionManager:

    def __init__(self):
        self.last_sync = None

    # =====================================================
    # Sync Position (Bybit → DB)
    # =====================================================
    def sync(self, symbol):

        logger.info("SYNC POSITION %s", symbol)

        position = get_position(symbol)

        # 포지션 없음
        if not position:
            delete_position(symbol)
            return None

        size = float(position.get("size", 0))

        # 포지션 종료 상태
        if size <= 0:
            delete_position(symbol)
            return None

        side = position.get("side", "")
        entry_price = float(position.get("avgPrice", 0))
        leverage = int(float(position.get("leverage", 1)))

        # DB 저장
        save_position(
            symbol=symbol,
            side=side,
            qty=size,
            entry_price=entry_price,
            leverage=leverage,
        )

        # PnL 업데이트
        pnl = get_unrealized_pnl(symbol)
        mark_price = get_last_price(symbol)

        update_position_price(
            symbol=symbol,
            mark_price=mark_price,
            unrealized_pnl=pnl,
        )

        self.last_sync = datetime.utcnow()

        return get_position(symbol)

    # =====================================================
    # Close Position (Market Close)
    # =====================================================
    def close(self, symbol):

        logger.info("CLOSE POSITION %s", symbol)

        result = close_position(symbol)

        # DB 즉시 삭제
        delete_position(symbol)

        return result

    # =====================================================
    # Is Open Check
    # =====================================================
    def is_open(self, symbol):

        pos = get_position(symbol)

        if not pos:
            return False

        return float(pos.get("size", 0)) > 0

    # =====================================================
    # Has Position (alias)
    # =====================================================
    def has_position(self, symbol):
        return self.is_open(symbol)

    # =====================================================
    # Refresh
    # =====================================================
    def refresh(self, symbol):
        return self.sync(symbol)

    # =====================================================
    # PnL
    # =====================================================
    def pnl(self, symbol):
        return get_unrealized_pnl(symbol)

    # =====================================================
    # Status (Dashboard)
    # =====================================================
    def status(self):

        return {
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
            "active": True,
        }

    # =====================================================
    # Health Check
    # =====================================================
    def health(self):

        return {
            "engine": "PositionManager",
            "healthy": True,
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
        }

    # =====================================================
    # Debug
    # =====================================================
    def __repr__(self):

        return f"<PositionManager last_sync={self.last_sync}>"
    

# =====================================================
# Singleton
# =====================================================
position_manager = PositionManager()
