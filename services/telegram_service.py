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

from risk.risk_engine import allow_trade

from services.telegram_service import (
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
            raise RuntimeError("Trade rate limit exceeded")

    # =====================================================
    # Duplicate Position
    # =====================================================
    def _position_check(self, symbol, signal):

        if not is_position_open(symbol):
            return

        raise RuntimeError("Position already exists.")

    # =====================================================
    # Execute
    # =====================================================
    def execute(self, signal, symbol, qty, strategy="", regime=""):

        with self.lock:

            logger.info("EXECUTE %s %s qty=%s", signal, symbol, qty)

            self._rate_limit()
            self._position_check(symbol, signal)

            if not allow_trade():
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

                order = execute_market(signal, symbol, qty)

                if not order.get("success", False):
                    return order

                order_id = ""

                try:
                    order_id = (
                        order["response"]
                        .get("result", {})
                        .get("orderId", "")
                    )
                except Exception:
                    logger.exception("order id parse failed")

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

                send_trade(signal, symbol, qty, price)

                self.last_execution = datetime.utcnow()

                logger.info("TRADE SAVED id=%s", trade.id)

                return {
                    "success": True,
                    "trade_id": trade.id,
                    "order_id": order_id,
                    "price": price,
                }

            except Exception as e:
                logger.exception(e)
                send_error(str(e))

                return {
                    "success": False,
                    "error": str(e),
                }


engine = ExecutionEngine()
