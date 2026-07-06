import logging
from datetime import datetime

from core.mode import mode_manager
from api.bybit_client import bybit_client
from execution.paper_engine import paper_engine

logger = logging.getLogger(__name__)


class OrderManager:

    def __init__(self):
        self.orders = {}

    def place_order(self, symbol, side, qty, price):

        # ======================
        # PAPER MODE
        # ======================
        if mode_manager.is_paper():

            return paper_engine.place_order(
                symbol, side, qty, price
            )

        # ======================
        # LIVE MODE
        # ======================
        resp = bybit_client.place_order(symbol, side, qty)

        order_id = resp.get("result", {}).get("orderId")

        self.orders[order_id] = {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "status": "PENDING",
            "created_at": datetime.utcnow()
        }

        return resp

    def sync(self):

        if mode_manager.is_paper():
            return

        for oid in list(self.orders.keys()):
            self.orders[oid]["status"] = "FILLED"


order_manager = OrderManager()
