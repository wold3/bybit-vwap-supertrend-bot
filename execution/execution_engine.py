from api.bybit_client import bybit
from execution.paper_engine import paper
from core.mode import mode
from risk.risk_engine import risk
from execution.order_lifecycle import lifecycle
from database.repository import trade_db


class Execution:

    def execute(self, symbol, side, qty, price):

        if not risk.allow():
            return None

        # ================================
        # ORDER 실행
        # ================================
        if mode.is_paper():
            res = paper.order(symbol, side, qty, price)
        else:
            res = bybit.order(symbol, side, qty)

        oid = res.get("result", {}).get("orderId")

        # ================================
        # PnL (간단 계산)
        # ================================
        pnl = 0.0

        # ================================
        # DB 저장 (핵심 추가)
        # ================================
        trade_db.insert(symbol, side, qty, price, pnl)

        # ================================
        # lifecycle 등록
        # ================================
        if oid:
            lifecycle.create(oid, symbol, side, qty, price)

        risk.add_trade()

        return res


engine = Execution()
