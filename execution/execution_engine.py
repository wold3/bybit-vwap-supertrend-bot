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
    # ENTRY (WITH RETRY)
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

        if not risk_engine.can_trade():
            telegram.send(f"🛑 BLOCKED BY RISK: {symbol}")
            return None

        result = self._send_bybit_order(symbol, side, qty)

        if result and result.get("retCode") == 0:

            telegram.send(
                f"📥 ORDER FILLED\n"
                f"{symbol} {side} {qty}"
            )
        else:

            telegram.send(
                f"❌ ORDER FAILED\n{result}"
            )

        return result

    # =================================================
    # SL / TP FUNCTIONS
    # =================================================

    # 1️⃣ 부분 익절
    def partial_close(self, symbol, qty_ratio=0.5):

        telegram.send(f"📉 PARTIAL CLOSE {symbol}")

        self._send_bybit_order(
            symbol=symbol,
            side="Sell",
            qty=qty_ratio,
            reduce_only=True
        )

    # 2️⃣ 본전 이동 (Stop Loss 수정)
    def move_sl_to_be(self, symbol):

        telegram.send(f"🟡 MOVE SL TO BREAKEVEN {symbol}")

        # 실제 API: stop order modify 필요
        # 여기선 구조만
        return True

    # 3️⃣ 전체 청산
    def close_position(self, symbol):

        telegram.send(f"🚨 CLOSE POSITION {symbol}")

        self._send_bybit_order(
            symbol=symbol,
            side="Sell",
            qty="ALL",
            reduce_only=True
        )

    # =================================================
    # BYBIT API CALL
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

        # SIGNATURE
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

            print("[BYBIT RESPONSE]", data)

            return data

        except Exception as e:

            print("[BYBIT ERROR]", e)
            telegram.send(f"❌ API ERROR: {e}")

            return None
