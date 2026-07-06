class OrderLifecycle:

    def __init__(self):
        self.orders = {}

    # =====================================================
    # CREATE
    # =====================================================
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

    # =====================================================
    # PARTIAL / FILL UPDATE
    # =====================================================
    def update_fill(self, oid, fill_qty, fill_price):

        order = self.orders.get(oid)
        if not order:
            return

        prev_qty = order["filled_qty"]

        new_qty = prev_qty + fill_qty

        # avg price 계산
        order["avg_price"] = (
            (order["avg_price"] * prev_qty +
             fill_price * fill_qty)
            / new_qty
        )

        order["filled_qty"] = new_qty

        if new_qty >= order["qty"]:
            order["status"] = "FILLED"
        else:
            order["status"] = "PARTIAL"

    # =====================================================
    # CANCEL
    # =====================================================
    def cancel(self, oid):

        if oid in self.orders:
            self.orders[oid]["status"] = "CANCELED"

    # =====================================================
    # REJECT
    # =====================================================
    def reject(self, oid):

        if oid in self.orders:
            self.orders[oid]["status"] = "REJECTED"

    # =====================================================
    # GET
    # =====================================================
    def get(self, oid):
        return self.orders.get(oid)


lifecycle = OrderLifecycle()
