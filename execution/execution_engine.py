import logging
import threading
import time
from datetime import datetime

from api.bybit_api import (
    execute_market,
    get_last_price,
    is_position_open,
)

from database.repository import (
    add_trade,
    update_bot_state,
)

from risk_engine import (
    allow_trade,
)

from telegram import (
    send_error,
    send_trade,
)

logger = logging.getLogger(__name__)


class ExecutionEngine:

    def __init__(self):

        self.lock = threading.Lock()

        self.last_execution = None

        self.execution_count = 0

        self.execution_window = time.time()

    # =====================================================
    # Rate Limit
    # =====================================================

    def _rate_limit(self):

        now = time.time()

        if now - self.execution_window > 60:

            self.execution_window = now

            self.execution_count = 0

        self.execution_count += 1

        if self.execution_count > 3:

            raise RuntimeError(
                "Trade rate limit exceeded"
            )

    # =====================================================
    # Duplicate Position
    # =====================================================

    def _position_check(
        self,
        symbol,
        signal,
    ):

        if not is_position_open(symbol):
            return

        logger.warning(
            "%s already has open position",
            symbol,
        )

        raise RuntimeError(
            "Position already exists."
        )

    # =====================================================
    # Execute
    # =====================================================

    def execute(
        self,
        signal,
        symbol,
        qty,
        strategy="",
        regime="",
    ):

        with self.lock:

            logger.info(
                "EXECUTE %s %s qty=%s",
                signal,
                symbol,
                qty,
            )

            self._rate_limit()

            self._position_check(
                symbol,
                signal,
            )

            if not allow_trade():

                logger.warning(
                    "Risk engine rejected trade."
                )

                return {
                    "success": False,
                    "error": "Risk rejected",
                }

            try:

                price = get_last_price(symbol)

                if price is None:

                    return {
                        "success": False,
                        "error": "Price unavailable",
                    }

                order = execute_market(
                    signal,
                    symbol,
                    qty,
                )

                if not order.get("success", False):

                    logger.error(
                        "Order execution failed."
                    )

                    return order

                order_id = ""

                try:

                    order_id = (
                        order["response"]
                        .get("result", {})
                        .get("orderId", "")
                    )

                except Exception:

                    logger.exception(
                        "Failed to parse order id."
                    )

                trade = add_trade(
                    symbol=symbol,
                    side=signal,
                    qty=qty,
                    price=price,
                    strategy=strategy,
                    regime=regime,
                    order_id=order_id,
                )

                update_bot_state(
                    running=True,
                    signal=signal,
                    price=price,
                )

                send_trade(
                    signal=signal,
                    symbol=symbol,
                    qty=qty,
                    price=price,
                )

                self.last_execution = (
                    datetime.utcnow()
                )

                logger.info(
                    "Trade Saved : %s",
                    trade.id,
                )

                logger.info(
                    "Execution Completed"
                )

                return {
                    "success": True,
                    "trade_id": trade.id,
                    "order_id": order_id,
                    "price": price,
                    "order": order,
                }

            except Exception as e:

                logger.exception(e)

                send_error(str(e))

                return {
                    "success": False,
                    "error": str(e),
                }

    # =====================================================
    # Retry
    # =====================================================

    def execute_retry(
        self,
        signal,
        symbol,
        qty,
        strategy="",
        regime="",
        retry=3,
    ):

        last_error = None

        for attempt in range(1, retry + 1):

            logger.info(
                "Retry %s/%s",
                attempt,
                retry,
            )

            result = self.execute(
                signal=signal,
                symbol=symbol,
                qty=qty,
                strategy=strategy,
                regime=regime,
            )

            if result["success"]:

                return result

            last_error = result.get(
                "error",
                "Unknown Error",
            )

            time.sleep(2)

        return {
            "success": False,
            "error": last_error,
        }

    # =====================================================
    # Engine Status
    # =====================================================

    def status(self):

        return {

            "running": True,

            "last_execution": (
                self.last_execution.isoformat()
                if self.last_execution
                else None
            ),

            "execution_count": self.execution_count,

            "window_start": self.execution_window,
        }

    # =====================================================
    # Reset Counter
    # =====================================================

    def reset_counter(self):

        self.execution_count = 0

        self.execution_window = time.time()

    # =====================================================
    # Health Check
    # =====================================================

    def health(self):

        return {

            "engine": "ExecutionEngine",

            "healthy": True,

            "locked": self.lock.locked(),

            "last_execution": (
                self.last_execution.isoformat()
                if self.last_execution
                else None
            ),
        }

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self):

        return {

            "executions": self.execution_count,

            "last_execution": (
                self.last_execution.isoformat()
                if self.last_execution
                else None
            ),

            "uptime_window": round(
                time.time() - self.execution_window,
                2,
            ),
        }

    # =====================================================
    # Last Execution
    # =====================================================

    def last_execution_time(self):

        return self.last_execution

    # =====================================================
    # Is Busy
    # =====================================================

    def is_busy(self):

        return self.lock.locked()

    # =====================================================
    # Shutdown
    # =====================================================

    def shutdown(self):

        logger.info(
            "Execution Engine Shutdown"
        )

    # =====================================================
    # Startup
    # =====================================================

    def startup(self):

        logger.info(
            "Execution Engine Started"
        )

    # =====================================================
    # __repr__
    # =====================================================

    def __repr__(self):

        return (
            f"<ExecutionEngine "
            f"executions={self.execution_count} "
            f"last_execution={self.last_execution}>"
        )


# =====================================================
# Singleton
# =====================================================

engine = ExecutionEngine()


# =====================================================
# Module API
# =====================================================

__all__ = [
    "ExecutionEngine",
    "engine",
]
