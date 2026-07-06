import logging
import time

from execution.execution_engine import engine
from api.bybit_api import get_last_price, get_positions
from database.repository import update_position_price, get_positions as db_positions

logger = logging.getLogger(__name__)


class RecoveryManager:

    def __init__(self):

        self.retry_limit = 3
        self.retry_delay = 2

    # =====================================================
    # Order Retry
    # =====================================================
    def retry_order(self, func, *args, **kwargs):

        last_error = None

        for i in range(self.retry_limit):

            try:

                result = func(*args, **kwargs)

                if result and result.get("success"):
                    return result

            except Exception as e:

                last_error = str(e)
                logger.error("Retry error: %s", e)

            time.sleep(self.retry_delay)

        return {
            "success": False,
            "error": last_error or "retry_failed"
        }

    # =====================================================
    # Sync Positions
    # =====================================================
    def sync_positions(self):

        try:

            api_positions = get_positions()
            db_pos = db_positions()

            for p in api_positions:

                symbol = p.get("symbol")
                size = float(p.get("size", 0))

                if size <= 0:
                    continue

                price = get_last_price(symbol)
                pnl = float(p.get("unrealisedPnl", 0))

                update_position_price(
                    symbol=symbol,
                    mark_price=price,
                    unrealized_pnl=pnl,
                )

            logger.info("Position sync completed")

        except Exception as e:

            logger.error("Sync failed: %s", e)

    # =====================================================
    # Engine Recovery
    # =====================================================
    def recover_engine(self):

        try:

            status = engine.status()

            if not status.get("running"):

                logger.warning("Engine stopped, restarting...")

                engine.startup()

            return True

        except Exception as e:

            logger.error("Engine recovery failed: %s", e)

            return False

    # =====================================================
    # Full Recovery
    # =====================================================
    def full_recovery(self):

        logger.info("Starting full recovery")

        self.recover_engine()
        self.sync_positions()

        logger.info("Recovery completed")


# =====================================================
# Singleton
# =====================================================
recovery_manager = RecoveryManager()
