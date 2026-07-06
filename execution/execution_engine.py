import os
import time
import asyncio
import requests
import hmac
import hashlib
import json

from database.trade_db import trade_db
from services.ws_server import broadcast


# =====================================================
# 🔥 BYBIT REAL EXECUTION ENGINE
# =====================================================
class BybitExecutionEngine:

    def __init__(self):

        self.api_key = os.getenv("BYBIT_API_KEY", "")
        self.api_secret = os.getenv("BYBIT_API_SECRET", "")
        self.base_url = "https://api.bybit.com"

    # =================================================
    # SIGNATURE
    # =================================================
    def _sign(self, params: dict) -> str:

        param_str = "&".join(f"{k}={params[k]}" for k in sorted(params))

        return hmac.new(
            self.api_secret.encode(),
            param_str.encode(),
            hashlib.sha256
        ).hexdigest()

    # =================================================
    # MARKET ORDER
    # =================================================
    def execute(self, symbol, side, qty, price=None):

        timestamp = int(time.time() * 1000)

        endpoint = "/v5/order/create"

        params = {
            "category": "linear",
            "symbol": symbol,
            "side": side.capitalize(),  # Buy / Sell
            "orderType": "Market",
            "qty": str(qty),
            "timeInForce": "IOC",
            "timestamp": str(timestamp),
            "api_key": self.api_key
        }

        params["sign"] = self._sign(params)

        url = self.base_url + endpoint

        try:
            res = requests.post(url, json=params, timeout=5)
            data = res.json()

            # =========================================
            # ORDER ID
            # =========================================
            order_id = None

            try:
                order_id = data["result"]["orderId"]
            except:
                pass

            # =========================================
            # PnL CALC (실전에서는 포지션 기반으로 교체)
            # =========================================
            pnl = self._calc_pnl(symbol)

            # =========================================
            # DB SAVE
            # =========================================
            trade_db.insert(symbol, side, qty, price or 0, pnl)

            try:
                trade_db.insert_pnl_history(pnl)
            except:
                pass

            # =========================================
            # WS PUSH
            # =========================================
            self._push_pnl(pnl)

            return {
                "success": True,
                "order_id": order_id,
                "raw": data
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }

    # =================================================
    # PnL CALC (TEMP)
    # =================================================
    def _calc_pnl(self, symbol):

        try:
            # TODO: 실제 position 기반으로 변경
            import random
            return round((random.random() - 0.5) * 10, 2)

        except:
            return 0.0

    # =================================================
    # WS PUSH
    # =================================================
    def _push_pnl(self, pnl):

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


# =====================================================
# SINGLETON
# =====================================================
engine = BybitExecutionEngine()
