import time
from datetime import datetime


class OrderLifecycleManager:

    def __init__(self):

        self.orders = {}

    # =====================================================
    # CREATE ORDER
    # =====================================================
    def create(self, order_id, symbol, side, qty, price):

        self.orders[order_id] = {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "entry_price": price,

            "status": "PENDING",

            "filled_qty": 0,
            "avg_price": 0,

            "created_at": datetime.utcnow()
        }

    # =====================================================
    # UPDATE FILL
    # =====================================================
    def update_fill(self, order_id, fill_qty, fill_price):

        order = self.orders.get(order_id)

        if not order:
            return

        total_qty = order["filled_qty"] + fill_qty

        order["avg_price"] = (
            (order["avg_price"] * order["filled_qty"] +
             fill_price * fill_qty)
            / total_qty
        )

        order["filled_qty"] = total_qty

        if order["filled_qty"] >= order["qty"]:
            order["status"] = "FILLED"
        else:
            order["status"] = "PARTIAL"

    # =====================================================
    # CLOSE ORDER
    # =====================================================
    def close(self, order_id):

        order = self.orders.get(order_id)

        if order:
            order["status"] = "CLOSED"

    # =====================================================
    # GET ORDER
    # =====================================================
    def get(self, order_id):
        return self.orders.get(order_id)


order_lifecycle = OrderLifecycleManager()
