import os
import time
import asyncio
import random

from database.trade_db import trade_db
from services.ws_server import broadcast

from portfolio.position_manager import position_manager
from risk.risk_engine import risk_engine


class BybitExecutionEngine:

    def __init__(self):

        self.symbol = os.getenv("SYMBOL", "BTCUSDT")

        # 포트폴리오 equity
        self.portfolio = {
            "BTCUSDT": 10000,
            "ETHUSDT": 10000,
            "SOLUSDT": 10000
        }

    # =================================================
    # EXECUTE
    # =================================================
    def execute(self, symbol, side, qty, price):

        if not risk_engine.can_trade():
            return None

        symbol = symbol or self.symbol

        entry_price = self._price()

        position_manager.open_position(symbol, side, qty, entry_price)

        pnl = position_manager.update_price(symbol, entry_price)

        # =========================================
        # SYMBOL별 EQUITY 업데이트
        # =========================================
        self.portfolio[symbol] += pnl

        trade_db.insert_equity(symbol, self.portfolio[symbol])

        trade_db.insert(symbol, side, qty, entry_price, pnl)

        self._push(pnl)

        return pnl

    # =================================================
    # PRICE MOCK
    # =================================================
    def _price(self):

        return 65000 + random.randint(-100, 100)

    # =================================================
    # TOTAL EQUITY
    # =================================================
    def get_total_equity(self):

        return sum(self.portfolio.values())

    # =================================================
    # WS PUSH
    # =================================================
    def _push(self, pnl):

        try:
            asyncio.run(
                broadcast({
                    "type": "pnl",
                    "value": pnl
                })
            )
        except:
            pass


engine = BybitExecutionEngine()
