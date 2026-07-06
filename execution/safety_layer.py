import time
import logging

from api.bybit_api import execute_market, get_last_price

logger = logging.getLogger(__name__)


class SafetyLayer:

    def __init__(self):

        self.last_order_time = 0
        self.cooldown = 2  # seconds
        self.max_retry = 3

    # =====================================================
    # Cooldown Check
    # =====================================================
    def _cooldown_check(self):

        now = time.time()

        if now - self.last_order_time < self.cooldown:
            raise Exception("Cooldown active")

        self.last_order_time = now

    # =====================================================
    # Safe Execute
    # =====================================================
    def safe_execute(
        self,
        signal,
        symbol,
        qty
    ):

        self._cooldown_check()

        price = get_last_price(symbol)

        if price is None:
            return {
                "success": False,
                "error": "No price data"
            }

        last_error = None

        for attempt in range(1, self.max_retry + 1):

            try:

                logger.info(
                    "Attempt %s execution %s %s",
                    attempt,
                    signal,
                    symbol,
                )

                order = execute_market(signal, symbol, qty)

                if order and order.get("success"):
                    return {
                        "success": True,
                        "order": order,
                        "price": price,
                        "attempt": attempt
                    }

                last_error = order

            except Exception as e:

                logger.error("Execution error: %s", e)
                last_error = str(e)

            time.sleep(1)

        return {
            "success": False,
            "error": last_error,
            "price": price
        }

    # =====================================================
    # Validate Order
    # =====================================================
    def validate_order(self, order):

        if not order:
            return False

        if not order.get("success"):
            return False

        return True


# =====================================================
# Singleton
# =====================================================
safety_layer = SafetyLayer()
