import logging

from api.bybit_client import bybit_client
from api.order_manager import order_manager
from risk.risk_engine import risk_engine

logger = logging.getLogger(__name__)


class ExecutionEngine:

    def __init__(self):
        self.busy = False

    def get_real_pnl(self, symbol):

        res = bybit_client.get_positions(symbol)

        items = res.get("result", {}).get("list", [])

        pnl = 0

        for p in items:
            if p.get("symbol") == symbol:
                pnl += float(p.get("unrealisedPnl", 0))

        return pnl

    def check_exit(self, symbol, price):

        pnl = self.get_real_pnl(symbol)

        if pnl <= -10:
            return "STOP_LOSS"

        if pnl >= 20:
            return "TAKE_PROFIT"

        return None

    def close_position(self, symbol, reason):

        order_manager.place_market_order(
            symbol=symbol,
            side="Sell",
            qty=1
        )

    def execute(self, signal, symbol, qty, price, leverage=1):

        self.busy = True

        try:

            if not risk_engine.allow_trade():
                return {"success": False, "reason": "risk_block"}

            order_id = order_manager.place_market_order(
                symbol=symbol,
                side=signal,
                qty=qty,
                leverage=leverage
            )

            if not order_id:
                return {"success": False, "reason": "order_failed"}

            risk_engine.add_trade()

            return {"success": True, "order_id": order_id}

        finally:
            self.busy = False


engine = ExecutionEngine()
