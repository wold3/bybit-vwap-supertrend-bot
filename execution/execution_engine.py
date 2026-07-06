import logging
from datetime import datetime

from api.bybit_api import (
    execute_market,
    get_last_price,
)
from database.repository import (
    add_trade,
    update_bot_state,
)
from telegram import (
    send_error,
    send_trade,
)

logger = logging.getLogger(__name__)


# =====================================================
# Execution Engine
# =====================================================

class ExecutionEngine:

    def __init__(self):

        self.last_execution = None

    # =================================================

    def execute(
        self,
        signal,
        symbol,
        qty,
        strategy="",
        regime="",
    ):

        logger.info(
            "EXECUTE %s %s qty=%s",
            signal,
            symbol,
            qty,
        )

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

            if not order["success"]:

                return order

            order_id = ""

            try:

                order_id = (
                    order["response"]
                    .get("result", {})
                    .get("orderId", "")
                )

            except Exception:

                pass

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
                signal,
                symbol,
                qty,
                price,
            )

            self.last_execution = datetime.utcnow()

            logger.info(
                "ORDER COMPLETE id=%s",
                trade.id,
            )

            return {
                "success": True,
                "trade_id": trade.id,
                "order": order,
            }

        except Exception as e:

            logger.exception(e)

            send_error(str(e))

            return {
                "success": False,
                "error": str(e),
            }


engine = ExecutionEngine()
