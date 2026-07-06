import logging

from risk.risk_engine import risk_engine
from execution.order_manager import order_manager

logger = logging.getLogger(__name__)


class ExecutionEngine:

    def execute(self, signal, symbol, qty, price):

        if not risk_engine.allow_trade():
            return {"success": False, "reason": "risk_block"}

        resp = order_manager.place_order(
            symbol=symbol,
            side=signal,
            qty=qty,
            price=price
        )

        risk_engine.add_trade()

        return {
            "success": True,
            "resp": resp
        }


engine = ExecutionEngine()
