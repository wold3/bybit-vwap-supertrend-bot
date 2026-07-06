import os
import time
import asyncio
import requests
import hmac
import hashlib

from database.trade_db import trade_db
from services.ws_server import broadcast
from portfolio.position_manager import position_manager


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

        # =========================
        # ENTRY PRICE MOCK (실제는 체결가 받아야함)
        # =========================
        entry_price = self._get_price()

        # =========================
        # POSITION OPEN
        # =========================
        position_manager.open_position(symbol, side, qty, entry_price)

        # =========================
        # PnL 계산
        # =========================
        pnl = position_manager.update_price(symbol, entry_price)

        # =========================
        # DB 저장
        # =========================
        trade_db.insert(symbol, side, qty, entry_price, pnl)

        # =========================
        # WS PUSH
        # =========================
        self._push(pnl)

        return {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "pnl": pnl
        }

    # =================================================
    # PRICE MOCK (나중에 WebSocket 가격으로 교체)
    # =================================================
    def _get_price(self):

        import random
        return 65000 + random.randint(-100, 100)

    # =================================================
    # EXIT CHECK (SL / TP)
    # =================================================
    def check_risk(self, symbol):

        result = position_manager.check_exit(symbol)

        if result == "STOP_LOSS":
            print("[EXIT] STOP LOSS")

            position_manager.close_position(symbol)

        elif result == "TAKE_PROFIT":
            print("[EXIT] TAKE PROFIT")

            position_manager.close_position(symbol)

        return result

    # =================================================
    # WS PUSH
    # =================================================
    def _push(self, pnl):

        try:
            asyncio.run(broadcast({
                "type": "pnl",
                "value": pnl,
                "time": time.time()
            }))
        except:
            pass


engine = BybitExecutionEngine()
