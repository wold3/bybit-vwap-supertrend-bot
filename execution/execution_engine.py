from api.bybit_client import bybit
from execution.paper_engine import paper
from core.mode import mode
from risk.risk_engine import risk
from execution.order_lifecycle import lifecycle
from database.repository import trade_db
from execution.pnl_engine import pnl_engine


class Execution:

    def execute(self, symbol, side, qty, price):

        if not risk.allow():
            return None

        # ================================
        # ORDER EXECUTION
        # ================================
        if mode.is_paper():
            res = paper.order(symbol, side, qty, price)
        else:
            res = bybit.order(symbol, side, qty)

        oid = res.get("result", {}).get("orderId")

        # ================================
        # PnL 계산
        # ================================
        pnl = pnl_engine.get(symbol)

        # ================================
        # DB 저장 (trade)
        # ================================
        trade_db.insert(symbol, side, qty, price, pnl)

        # ================================
        # DB 저장 (PnL history)
        # ================================
        trade_db.insert_pnl_history(pnl)

        # ================================
        # lifecycle
        # ================================
        if oid:
            lifecycle.create(oid, symbol, side, qty, price)

        risk.add_trade()

        return res


engine = Execution()
