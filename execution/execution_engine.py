import os
import time
import hmac
import hashlib
import requests

from risk.risk_engine import risk_engine
from execution.retry_engine import retry_engine
from telegram import telegram


class BybitExecutionEngine:

    def __init__(self):

        self.api_key = os.getenv("BYBIT_API_KEY")
        self.api_secret = os.getenv("BYBIT_API_SECRET")
        self.base_url = os.getenv("BYBIT_BASE_URL", "https://api.bybit.com")

    # =================================================
    # PUBLIC ENTRY (RETRY WRAPPED)
    # =================================================
    def execute(self, symbol, side, qty, price=None):

        return retry_engine.execute_with_retry(
            self._execute_order,
            symbol,
            side,
            qty,
            price
        )

    # =================================================
    # INTERNAL ORDER LOGIC
    # =================================================
    def _execute_order(self, symbol, side, qty, price=None):

        # 🚨 RISK CHECK FIRST
        if not risk_engine.can_trade():
            print("[EXECUTION] BLOCKED BY RISK ENGINE")

            telegram.send(
                f"🛑 TRADE BLOCKED (RISK)\n"
                f"Symbol: {symbol}\nSide: {side}"
            )

            return None

        # 실제 주문 실행
        result = self._send_bybit_order(symbol, side, qty)

        # 결과 처리
        if result and result.get("retCode") == 0:

            telegram.send(
                f"📥 ORDER SUCCESS\n"
                f"Symbol: {symbol}\n"
                f"Side: {side}\n"
                f"Qty: {qty}\n"
                f"OrderId: {result.get('result', {}).get('orderId')}"
            )

        else:

            telegram.send(
                f"❌ ORDER FAILED\n"
                f"Symbol: {symbol}\n"
                f"Side: {side}\n"
                f"Response: {result}"
            )

        return result

    # =================================================
    # BYBIT REST API CALL
    # =================================================
    def _send_bybit_order(self, symbol, side, qty):

        endpoint = "/v5/order/create"
        url = self.base_url + endpoint

        timestamp = str(int(time.time() * 1000))

        params = {
            "category": "linear",
            "symbol": symbol,
            "side": side,               # Buy / Sell
            "orderType": "Market",
            "qty": str(qty),
            "timeInForce": "IOC",
            "api_key": self.api_key,
            "timestamp": timestamp,
            "recv_window": "5000"
        }

        # =================================================
        # SIGNATURE
        # =================================================
        query_string = "&".join([f"{k}={params[k]}" for k in sorted(params)])

        signature = hmac.new(
            self.api_secret.encode(),
            query_string.encode(),
            hashlib.sha256
        ).hexdigest()

        params["sign"] = signature

        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=params, headers=headers, timeout=5)

            data = response.json()

            print("[BYBIT RESPONSE]", data)

            return data

        except Exception as e:

            print("[BYBIT ERROR]", e)

            telegram.send(f"❌ BYBIT API ERROR: {e}")

            return None
