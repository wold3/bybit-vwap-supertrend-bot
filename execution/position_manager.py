import logging
from datetime import datetime

from api.bybit_api import (
    close_position,
    get_position,
    get_last_price,
    get_unrealized_pnl,
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
    def sync(self, symbol: str):

        logger.info("SYNC POSITION %s", symbol)

        position = get_position(symbol)

        # 포지션 없음
        if not position:
            delete_position(symbol)
            return None

        size = float(position.get("size", 0))

        # 포지션 종료 상태
        if size == 0:
            delete_position(symbol)
            return None

        side = position.get("side", "")
        entry_price = float(position.get("avgPrice", 0))
        leverage = int(float(position.get("leverage", 1)))

        save_position(
            symbol=symbol,
            side=side,
            qty=size,
            entry_price=entry_price,
            leverage=leverage,
        )

        mark_price = get_last_price(symbol)
        pnl = get_unrealized_pnl(symbol)

        update_position_price(
            symbol=symbol,
            mark_price=mark_price,
            unrealized_pnl=pnl,
        )

        self.last_sync = datetime.utcnow()

        return get_position(symbol)

    # =====================================================
    # Close Position
    # =====================================================
    def close(self, symbol: str):

        logger.info("CLOSE POSITION %s", symbol)
        return close_position(symbol)

    # =====================================================
    # Check Position Open
    # =====================================================
    def is_open(self, symbol: str) -> bool:

        position = get_position(symbol)

        if not position:
            return False

        return float(position.get("size", 0)) > 0

    # =====================================================
    # Has Position (alias)
    # =====================================================
    def has_position(self, symbol: str) -> bool:
        return self.is_open(symbol)

    # =====================================================
    # Refresh
    # =====================================================
    def refresh(self, symbol: str):
        return self.sync(symbol)

    # =====================================================
    # PnL
    # =====================================================
    def pnl(self, symbol: str) -> float:

        return get_unrealized_pnl(symbol)

    # =====================================================
    # Close All (DB 기준)
    # =====================================================
    def close_all(self):

        logger.info("CLOSE ALL POSITIONS")

        # 실제 Bybit 청산은 개별 포지션 루프 필요
        # 여기서는 DB 기준 정리
        from database.repository import get_positions

        positions = get_positions()

        for p in positions:
            symbol = p.symbol if hasattr(p, "symbol") else None

            if symbol:
                try:
                    close_position(symbol)
                    delete_position(symbol)
                except Exception as e:
                    logger.exception(e)

        return True

    # =====================================================
    # Status
    # =====================================================
    def status(self):

        return {
            "last_sync": self.last_sync.isoformat()
            if self.last_sync
            else None,
        }

    # =====================================================
    # Health Check
    # =====================================================
    def health(self):

        return {
            "engine": "PositionManager",
            "healthy": True,
            "last_sync": self.last_sync.isoformat()
            if self.last_sync
            else None,
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


# =====================================================
# Export
# =====================================================
__all__ = [
    "PositionManager",
    "position_manager",
]
