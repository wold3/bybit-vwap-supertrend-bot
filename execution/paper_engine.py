import uuid


class PaperEngine:

    def __init__(self):
        self.positions = {}

    def order(self, symbol, side, qty, price):

        oid = str(uuid.uuid4())

        self.positions[symbol] = {
            "side": side,
            "qty": qty,
            "entry": price
        }

        return {"result": {"orderId": oid}}

paper = PaperEngine()
