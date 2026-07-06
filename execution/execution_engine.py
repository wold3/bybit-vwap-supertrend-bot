import uuid
from datetime import datetime


class PaperEngine:

    def __init__(self):
        self.positions = {}
        self.orders = {}

    def place_order(self, symbol, side, qty, price):

        order_id = str(uuid.uuid4())

        self.orders[order_id] = {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "price": price,
            "status": "FILLED",
            "time": datetime.utcnow()
        }

        self.positions[symbol] = {
            "side": side,
            "qty": qty,
            "entry": price
        }

        return {"result": {"orderId": order_id}}

    def get_positions(self, symbol):
        return self.positions.get(symbol)


paper_engine = PaperEngine()
