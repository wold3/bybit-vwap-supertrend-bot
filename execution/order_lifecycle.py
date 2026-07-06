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
            "filled_qty": 0
        }

    def fill(self, oid, qty, price):

        o = self.orders.get(oid)
        if not o:
            return

        o["filled_qty"] += qty

        if o["filled_qty"] >= o["qty"]:
            o["status"] = "FILLED"
        else:
            o["status"] = "PARTIAL"

    def close(self, oid):
        if oid in self.orders:
            self.orders[oid]["status"] = "CLOSED"


lifecycle = OrderLifecycle()
