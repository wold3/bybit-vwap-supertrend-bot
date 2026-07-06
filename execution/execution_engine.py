from api.bybit_client import bybit
from execution.paper_engine import paper
from core.mode import mode
from risk.risk_engine import risk
from execution.order_lifecycle import lifecycle


class Execution:

    def execute(self, symbol, side, qty, price):

        if not risk.allow():
            return None

        # =========================
        # PAPER / LIVE
        # =========================
        if mode.is_paper():
            res = paper.order(symbol, side, qty, price)
        else:
            res = bybit.order(symbol, side, qty)

        oid = res.get("result", {}).get("orderId")

        if not oid:
            return res

        lifecycle.create(oid, symbol, side, qty, price)

        risk.add_trade()

        return res


engine = Execution()
