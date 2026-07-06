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

from execution.execution_guard import execution_guard

from services.telegram_service import (
    send_error,
    send_trade,
)

from services.logger_service import logger


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
    # Position Check
    # =====================================================

    def _position_check(self, symbol, signal):

        if is_position_open(symbol):
            logger.warning("%s already has open position", symbol)
            raise RuntimeError("Position already exists")

    # =====================================================
    # Execute
    # =====================================================

    def execute(self, signal, symbol, qty, strategy="", regime=""):

        # 0. Execution Guard
        if not execution_guard.acquire():
            return {"success": False, "error": "engine_locked"}

        if not execution_guard.rate_limit():
            execution_guard.release()
            return {"success": False, "error": "rate_limited"}

        if not execution_guard.allow_symbol(symbol):
            execution_guard.release()
            return {"success": False, "error": "duplicate_symbol"}

        try:

            logger.info("EXECUTE %s %s qty=%s", signal, symbol, qty)

            self._rate_limit()
            self._position_check(symbol, signal)

            if not allow_trade():
                execution_guard.release()
                return {"success": False, "error": "risk_rejected"}

            price = get_last_price(symbol)

            if price is None:
                execution_guard.release()
                return {"success": False, "error": "price_unavailable"}

            order = execute_market(signal, symbol, qty)

            if not order.get("success", False):
                execution_guard.release()
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

            logger.info("Trade saved id=%s", trade.id)

            execution_guard.release()

            return {
                "success": True,
                "trade_id": trade.id,
                "order_id": order_id,
                "price": price,
            }

        except Exception as e:

            logger.exception(e)
            send_error(str(e))

            execution_guard.release()

            return {"success": False, "error": str(e)}

    # =====================================================
    # Retry
    # =====================================================

    def execute_retry(self, *args, retry=3, **kwargs):

        last_error = None

        for i in range(retry):

            result = self.execute(*args, **kwargs)

            if result.get("success"):
                return result

            last_error = result.get("error")

            time.sleep(2)

        return {"success": False, "error": last_error}

    # =====================================================
    # Status
    # =====================================================

    def status(self):

        return {
            "execution_count": self.execution_count,
            "last_execution": (
                self.last_execution.isoformat()
                if self.last_execution
                else None
            ),
        }


engine = ExecutionEngine()
