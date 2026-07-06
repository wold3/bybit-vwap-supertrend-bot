class OrderLifecycle:

    def __init__(self):
        self.orders = {}

    def create(self, oid, symbol, side, qty, price):

        self.orders[oid] = {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "price": price,
            "status": "PENDING"
        }

    def fill(self, oid):
        if oid in self.orders:
            self.orders[oid]["status"] = "FILLED"

    def get(self, oid):
        return self.orders.get(oid)


lifecycle = OrderLifecycle()
