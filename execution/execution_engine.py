import os
import time
import asyncio
import requests
import hmac
import hashlib

from database.trade_db import trade_db
from services.ws_server import broadcast

from portfolio.position_manager import position_manager
from risk.risk_engine import risk_engine


class BybitExecutionEngine:

    def __init__(self):

        self.api_key = os.getenv("BYBIT_API_KEY")
        self.api_secret = os.getenv("BYBIT_API_SECRET")
        self.base_url = "https://api.bybit.com"

        self.symbol = os.getenv("SYMBOL", "BTCUSDT")

    # =================================================
    # EXECUTE ORDER
    # =================================================
    def execute(self, symbol, side, qty, price):

        symbol = symbol or self.symbol

        # =================================================
        # 🚨 GLOBAL RISK GATE (핵심)
        # =================================================
        if not risk_engine.can_trade():
            print("[EXECUTION] BLOCKED BY RISK ENGINE")
            return None

        # =================================================
        # ENTRY PRICE (mock or replace with real fill price)
        # =================================================
        entry_price = self._get_price()

        # =================================================
        # POSITION OPEN
        # =================================================
        position_manager.open_position(symbol, side, qty, entry_price)

        # =================================================
        # PnL CALC
        # =================================================
        pnl = position_manager.update_price(symbol, entry_price)

        # =================================================
        # RISK ENGINE UPDATE (핵심 연결)
        # =================================================
        risk_engine.update_pnl(pnl)

        # =================================================
        # DB SAVE
        # =================================================
        trade_db.insert(symbol, side, qty, entry_price, pnl)

        try:
            trade_db.insert_pnl_history(pnl)
        except:
            pass

        # =================================================
        # WS PUSH
        # =================================================
        self._push(pnl)

        return {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "pnl": pnl
        }

    # =================================================
    # PRICE MOCK
    # =================================================
    def _get_price(self):

        import random
        return 65000 + random.randint(-100, 100)

    # =================================================
    # WS PUSH
    # =================================================
    def _push(self, pnl):

        try:
            asyncio.run(
                broadcast({
                    "type": "pnl",
                    "value": pnl,
                    "time": time.time()
                })
            )
        except:
            pass


# SINGLETON
engine = BybitExecutionEngine()
