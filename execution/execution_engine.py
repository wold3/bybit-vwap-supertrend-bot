import logging

from risk.risk_engine import risk_engine
from api.bybit_client import bybit_client
from execution.order_lifecycle import order_lifecycle
from execution.pnl_engine import pnl_engine

logger = logging.getLogger(__name__)


class ExecutionEngine:

    def execute(self, signal, symbol, qty, price):

        if not risk_engine.allow_trade():
            return {"success": False, "reason": "risk_block"}

        resp = bybit_client.place_order(
            symbol=symbol,
            side=signal,
            qty=qty
        )

        order_id = resp.get("result", {}).get("orderId")

        if order_id:

            order_lifecycle.create(
                order_id,
                symbol,
                signal,
                qty,
                price
            )

        risk_engine.add_trade()

        return {
            "success": True,
            "order_id": order_id
        }

    # =====================================================
    # REAL PnL UPDATE
    # =====================================================
    def update_pnl(self, symbol):

        pnl_data = pnl_engine.get_position_pnl(symbol)

        risk_engine.update_pnl(pnl_data["pnl"])

        return pnl_data


engine = ExecutionEngine()
