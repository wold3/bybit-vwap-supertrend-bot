
import os
import time
import hmac
import hashlib
import requests

from risk.risk_engine import risk_engine
from risk.drawdown_guard import drawdown_guard
from execution.retry_engine import retry_engine
from telegram import telegram


class BybitExecutionEngine:

    def __init__(self):

        self.api_key = os.getenv("BYBIT_API_KEY")
        self.api_secret = os.getenv("BYBIT_API_SECRET")
        self.base_url = os.getenv("BYBIT_BASE_URL", "https://api.bybit.com")

    # =================================================
    # ENTRY WRAPPER
    # =================================================
    def execute(self, symbol, side, qty):

        return retry_engine.execute_with_retry(
            self._execute_order,
            symbol,
            side,
            qty
        )

    # =================================================
    # CORE ORDER
    # =================================================
    def _execute_order(self, symbol, side, qty):

        # ============================================
        # 1. RISK CHECK
        # ============================================
        if not risk_engine.can_trade():

            print("[BLOCK] RISK ENGINE")

            telegram.send("🛑 BLOCKED BY RISK ENGINE")

            return None

        # ============================================
        # 2. DRAWDOWN CHECK (핵심 추가)
        # ============================================
        if not drawdown_guard.can_trade():

            print("[BLOCK] DRAWDOWN LIMIT HIT")

            telegram.send("🚨 BLOCKED BY DRAWDOWN LIMIT")

            return None

        # ============================================
        # 3. ORDER SEND
        # ============================================
        result = self._send_bybit_order(symbol, side, qty)

        # ============================================
        # 4. RESPONSE LOG
        # ============================================
        if result and result.get("retCode") == 0:

            telegram.send(f"📥 ORDER FILLED {symbol} {side} {qty}")

        else:

            telegram.send(f"❌ ORDER FAILED {result}")

        return result

    # =================================================
    # BYBIT ORDER API
    # =================================================
    def _send_bybit_order(self, symbol, side, qty, reduce_only=False):

        endpoint = "/v5/order/create"
        url = self.base_url + endpoint

        timestamp = str(int(time.time() * 1000))

        params = {
            "category": "linear",
            "symbol": symbol,
            "side": side,
            "orderType": "Market",
            "qty": str(qty),
            "timeInForce": "IOC",
            "api_key": self.api_key,
            "timestamp": timestamp,
            "recv_window": "5000"
        }

        if reduce_only:
            params["reduceOnly"] = True

        query = "&".join([f"{k}={params[k]}" for k in sorted(params)])

        signature = hmac.new(
            self.api_secret.encode(),
            query.encode(),
            hashlib.sha256
        ).hexdigest()

        params["sign"] = signature

        try:
            res = requests.post(url, json=params, timeout=5)
            data = res.json()

            print("[BYBIT]", data)

            return data

        except Exception as e:

            print("[ERROR]", e)
            telegram.send(f"❌ API ERROR: {e}")

            return None
