import logging
from datetime import datetime

from api.bybit_api import (
    close_position,
    get_last_price,
    get_position,
    get_unrealized_pnl,
)

from database.repository import (
    delete_position,
    save_position,
    update_position_price,
)

logger = logging.getLogger(__name__)


class PositionManager:

    def __init__(self):

        self.last_sync = None

    # =====================================================
    # Sync Position
    # =====================================================

    def sync(self, symbol):

        logger.info(
            "Sync Position : %s",
            symbol,
        )

        position = get_position(symbol)

        if position is None:

            delete_position(symbol)

            return None

        size = float(
            position.get("size", 0)
        )

        if size == 0:

            delete_position(symbol)

            return None

        side = position.get("side")

        entry_price = float(
            position.get(
                "avgPrice",
                0,
            )
        )

        leverage = int(
            float(
                position.get(
                    "leverage",
                    1,
                )
            )
        )

        save_position(
            symbol=symbol,
            side=side,
            qty=size,
            entry_price=entry_price,
            leverage=leverage,
        )

        pnl = get_unrealized_pnl(symbol)

        price = get_last_price(symbol)

        update_position_price(
            symbol=symbol,
            mark_price=price,
            unrealized_pnl=pnl,
        )

        self.last_sync = datetime.utcnow()

        logger.info(
            "Position synced."
        )

        return get_position(symbol)

    # =====================================================
    # Close Position
    # =====================================================

    def close(self, symbol):

        logger.info(
            "Close Position : %s",
            symbol,
        )

        return close_position(symbol)

    # =====================================================
    # Is Open
    # =====================================================

    def is_open(self, symbol):

        position = get_position(symbol)

        if position is None:

            return False

        return float(
            position.get(
                "size",
                0,
            )
        ) > 0

    # =====================================================
    # Has Position
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
    # Summary
    # =====================================================

    def summary(self, symbol):

        position = get_position(symbol)

        if position is None:

            return {
                "open": False,
            }

        return {

            "open": True,

            "side": position.get(
                "side"
            ),

            "size": float(
                position.get(
                    "size",
                    0,
                )
            ),

            "entry_price": float(
                position.get(
                    "avgPrice",
                    0,
                )
            ),

            "mark_price": get_last_price(
                symbol
            ),

            "unrealized_pnl": get_unrealized_pnl(
                symbol
            ),

            "last_sync": (
                self.last_sync.isoformat()
                if self.last_sync
                else None
            ),
        }

    # =====================================================
    # Close Multiple Positions
    # =====================================================

    def close_all(self, symbols):

        results = []

        for symbol in symbols:

            try:

                result = self.close(symbol)

                results.append(
                    {
                        "symbol": symbol,
                        "success": True,
                        "result": result,
                    }
                )

            except Exception as e:

                logger.exception(e)

                results.append(
                    {
                        "symbol": symbol,
                        "success": False,
                        "error": str(e),
                    }
                )

        return results

    # =====================================================
    # Status
    # =====================================================

    def status(self):

        return {

            "engine": "PositionManager",

            "healthy": True,

            "last_sync": (
                self.last_sync.isoformat()
                if self.last_sync
                else None
            ),
        }

    # =====================================================
    # Health
    # =====================================================

    def health(self):

        return self.status()

    # =====================================================
    # __repr__
    # =====================================================

    def __repr__(self):

        return (
            f"<PositionManager "
            f"last_sync={self.last_sync}>"
        )


# =====================================================
# Singleton
# =====================================================

position_manager = PositionManager()


# =====================================================
# Module Export
# =====================================================

__all__ = [
    "PositionManager",
    "position_manager",
]
