import asyncio
from database.trade_db import trade_db
from services.ws_server import broadcast


class ExecutionEngine:

    def execute(self, symbol, side, qty, price):

        # ============================
        # MOCK PnL (실거래 붙일 자리)
        # ============================
        pnl = self.calc_pnl(symbol)

        # ============================
        # DB 저장
        # ============================
        trade_db.insert(symbol, side, qty, price, pnl)

        try:
            trade_db.insert_pnl_history(pnl)
        except:
            pass

        # ============================
        # WS PUSH (핵심)
        # ============================
        self.push_pnl(pnl)

        return {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "pnl": pnl
        }

    # ============================
    # PnL 계산
    # ============================
    def calc_pnl(self, symbol):
        return round((0.5 - __import__("random").random()) * 10, 2)

    # ============================
    # WS PUSH
    # ============================
    def push_pnl(self, pnl):

        try:
            asyncio.run(broadcast({
                "type": "pnl",
                "value": pnl
            }))
        except:
            pass


engine = ExecutionEngine()
