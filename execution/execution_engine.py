import logging

from api.bybit_client import bybit_client
from risk.risk_engine import risk_engine
from execution.orderbook_engine import orderbook_engine

logger = logging.getLogger(__name__)


class ExecutionEngine:

    def __init__(self):
        self.busy = False

    def execute(self, signal, symbol, qty, price):

        self.busy = True

        try:

            if not risk_engine.allow_trade():
                return {"success": False, "reason": "risk_block"}

            mid = orderbook_engine.mid_price(symbol)

            if mid:

                slippage = abs(price - mid) / mid

                if slippage > 0.005:
                    return {"success": False, "reason": "high_slippage"}

            resp = bybit_client.place_order(
                symbol=symbol,
                side=signal,
                qty=qty
            )

            risk_engine.add_trade()

            return {"success": True, "resp": resp}

        finally:
            self.busy = False


engine = ExecutionEngine()
