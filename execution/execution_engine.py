import os
import time
import asyncio
import requests
import hmac
import hashlib

from database.trade_db import trade_db
from services.ws_server import broadcast


class BybitExecutionEngine:

    def __init__(self):

        # =========================
        # 🔥 ENV ONLY CONFIG
        # =========================
        self.api_key = os.getenv("BYBIT_API_KEY")
        self.api_secret = os.getenv("BYBIT_API_SECRET")
        self.base_url = "https://api.bybit.com"

        self.symbol = os.getenv("SYMBOL", "BTCUSDT")

        if not self.api_key or not self.api_secret:
            raise Exception("❌ BYBIT API KEY NOT SET IN ENV")

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
    # EXECUTE ORDER
    # =================================================
    def execute(self, symbol, side, qty, price=None):

        timestamp = int(time.time() * 1000)

        params = {
            "category": "linear",
            "symbol": symbol or self.symbol,
            "side": side.capitalize(),
            "orderType": "Market",
            "qty": str(qty),
            "timeInForce": "IOC",
            "timestamp": str(timestamp),
            "api_key": self.api_key
        }

        params["sign"] = self._sign(params)

        try:
            res = requests.post(
                self.base_url + "/v5/order/create",
                json=params,
                timeout=5
            )

            data = res.json()

            order_id = data.get("result", {}).get("orderId")

            pnl = self._calc_pnl()

            trade_db.insert(symbol, side, qty, price or 0, pnl)

            try:
                trade_db.insert_pnl_history(pnl)
            except:
                pass

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
    # MOCK PnL (later replace with real position PnL)
    # =================================================
    def _calc_pnl(self):

        import random
        return round((random.random() - 0.5) * 10, 2)

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


# =========================
# SINGLETON
# =========================
engine = BybitExecutionEngine()
