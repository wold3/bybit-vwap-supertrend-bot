class OrderLifecycle:

    def __init__(self):
        self.orders = {}

    def create(self, oid, symbol, side, qty, price):

        self.orders[oid] = {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "price": price,
            "status": "PENDING",
            "filled_qty": 0,
            "avg_price": 0.0
        }

    def update_fill(self, oid, qty, price):

        o = self.orders.get(oid)
        if not o:
            return

        prev = o["filled_qty"]
        new = prev + qty

        o["avg_price"] = (
            (o["avg_price"] * prev + price * qty) / new
        )

        o["filled_qty"] = new

        o["status"] = "FILLED" if new >= o["qty"] else "PARTIAL"

    def close(self, oid):
        if oid in self.orders:
            self.orders[oid]["status"] = "CLOSED"

lifecycle = OrderLifecycle()
