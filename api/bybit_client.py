import time
import hmac
import hashlib
import requests
import json

from config import BYBIT_API_KEY, BYBIT_API_SECRET, BYBIT_TESTNET


class BybitClient:

    def __init__(self):

        self.api_key = BYBIT_API_KEY
        self.api_secret = BYBIT_API_SECRET

        if BYBIT_TESTNET:
            self.base_url = "https://api-testnet.bybit.com"
        else:
            self.base_url = "https://api.bybit.com"

    # =====================================================
    # SIGNATURE (FIXED - V5 STANDARD)
    # =====================================================

    def _sign(self, timestamp, recv_window, payload):

        param_str = timestamp + self.api_key + str(recv_window) + payload

        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            param_str.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        return signature

    # =====================================================
    # REQUEST
    # =====================================================

    def _request(self, method, endpoint, params=None):

        if params is None:
            params = {}

        timestamp = str(int(time.time() * 1000))
        recv_window = "5000"

        payload = json.dumps(params) if method == "POST" else ""

        signature = self._sign(timestamp, recv_window, payload)

        headers = {
            "X-BAPI-API-KEY": self.api_key,
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-SIGN": signature,
            "X-BAPI-RECV-WINDOW": recv_window,
            "Content-Type": "application/json"
        }

        url = self.base_url + endpoint

        try:

            if method == "GET":
                resp = requests.get(url, params=params, headers=headers, timeout=5)
            else:
                resp = requests.post(url, data=payload, headers=headers, timeout=5)

            data = resp.json()

            # =========================
            # 🔥 중요: 실패 감지
            # =========================
            if data.get("retCode") != 0:
                return {
                    "success": False,
                    "error": data,
                    "result": {}
                }

            return {
                "success": True,
                "result": data.get("result", {})
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e),
                "result": {}
            }

    # =====================================================
    # PRICE
    # =====================================================

    def get_price(self, symbol):

        return self._request(
            "GET",
            "/v5/market/tickers",
            {"category": "linear", "symbol": symbol}
        )

    # =====================================================
    # BALANCE
    # =====================================================

    def get_balance(self):

        return self._request(
            "GET",
            "/v5/account/wallet-balance",
            {"accountType": "UNIFIED"}
        )

    # =====================================================
    # ORDER
    # =====================================================

    def place_order(self, symbol, side, qty, leverage=1):

        params = {
            "category": "linear",
            "symbol": symbol,
            "side": side,
            "orderType": "Market",
            "qty": str(qty),
            "timeInForce": "GoodTillCancel"
        }

        return self._request(
            "POST",
            "/v5/order/create",
            params
        )


# =====================================================
# SINGLETON
# =====================================================

bybit_client = BybitClient()
