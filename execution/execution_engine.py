from api.bybit_client import bybit
from execution.paper_engine import paper
from core.mode import mode
from risk.risk_engine import risk
from execution.order_lifecycle import lifecycle
from database.repository import trade_db

# 🔥 WebSocket PnL push
from services.ws_server import broadcast
import asyncio


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
        # PnL 계산 (현재 구조 유지)
        # ================================
        pnl = self.calculate_pnl(symbol)

        # ================================
        # DB 저장
        # ================================
        trade_db.insert(symbol, side, qty, price, pnl)

        trade_db.insert_pnl_history(pnl)

        # ================================
        # lifecycle
        # ================================
        if oid:
            lifecycle.create(oid, symbol, side, qty, price)

        risk.add_trade()

        # ================================
        # 🔥 WebSocket PUSH (핵심 추가)
        # ================================
        self.push_pnl(pnl)

        return res

    # ================================
    # PnL 계산 함수 (기존 엔진 사용)
    # ================================
    def calculate_pnl(self, symbol):

        try:
            from execution.pnl_engine import pnl_engine
            return pnl_engine.get(symbol)
        except:
            return 0.0

    # ================================
    # 🔥 WS PUSH 함수
    # ================================
    def push_pnl(self, pnl):

        try:
            asyncio.run(
                broadcast({
                    "type": "pnl",
                    "value": pnl
                })
            )
        except Exception:
            # WS 없어도 거래는 멈추지 않게
            pass


engine = Execution()
