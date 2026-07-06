import os
import time
import json
import hmac
import hashlib
import requests

from risk.risk_engine import risk_engine
from telegram import telegram


class BybitExecutionEngine:

    def __init__(self):

        self.api_key = os.getenv("BYBIT_API_KEY")
        self.api_secret = os.getenv("BYBIT_API_SECRET")
        self.base_url = "https://api.bybit.com"

    # =================================================
    # SIGNATURE (필수)
    # =================================================
    def _sign(self, params: dict):

        ordered = "&".join([f"{k}={params[k]}" for k in sorted(params)])

        return hmac.new(
            self.api_secret.encode(),
            ordered.encode(),
            hashlib.sha256
        ).hexdigest()

    # =================================================
    # CREATE ORDER (REAL)
    # =================================================
    def execute(self, symbol, side, qty, price=None):

        if not risk_engine.can_trade():
            print("[EXECUTION] BLOCKED BY RISK")
            return None

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

        params["sign"] = self._sign(params)

        headers = {
            "Content-Type": "application/json"
        }

        try:
            res = requests.post(url, json=params, headers=headers, timeout=5)
            data = res.json()

            print("[BYBIT ORDER]", data)

            # =================================================
            # TELEGRAM ALERT
            # =================================================
            telegram.send(
                f"📊 ORDER EXECUTED\n"
                f"Symbol: {symbol}\n"
                f"Side: {side}\n"
                f"Qty: {qty}\n"
                f"Response: {data}"
            )

            return data

        except Exception as e:

            print("[ORDER ERROR]", e)

            telegram.send(f"❌ ORDER ERROR: {e}")

            return None
