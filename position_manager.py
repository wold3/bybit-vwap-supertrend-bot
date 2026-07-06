class PositionManager:

    def __init__(self):

        self.positions = {}

    # =================================================
    # OPEN POSITION
    # =================================================
    def open_position(self, symbol, side, qty, price):

        self.positions[symbol] = {
            "side": side,
            "qty": qty,
            "entry_price": price,
            "realized_pnl": 0
        }

    # =================================================
    # FILL UPDATE (핵심)
    # =================================================
    def update_fill(self, symbol, side, qty, price):

        if symbol not in self.positions:
            self.open_position(symbol, side, qty, price)
            return

        pos = self.positions[symbol]

        # 평균가 계산 (단순화)
        old_qty = pos["qty"]
        old_price = pos["entry_price"]

        new_qty = old_qty + qty

        if new_qty == 0:
            return

        new_price = (
            (old_qty * old_price + qty * price)
            / new_qty
        )

        pos["qty"] = new_qty
        pos["entry_price"] = new_price

    # =================================================
    # CURRENT POSITION
    # =================================================
    def get_position(self, symbol):

        return self.positions.get(symbol)


# SINGLETON
position_manager = PositionManager()
