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
    # SIGNATURE
    # =====================================================
    def _sign(self, params: dict):

        timestamp = str(int(time.time() * 1000))

        param_str = timestamp + self.api_key + json.dumps(params, separators=(',', ':'))

        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            param_str.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        return timestamp, signature

    # =====================================================
    # REQUEST (FIXED)
    # =====================================================
    def _request(self, method, endpoint, params=None):

        if params is None:
            params = {}

        try:
            timestamp, signature = self._sign(params)

            headers = {
                "X-BAPI-API-KEY": self.api_key,
                "X-BAPI-TIMESTAMP": timestamp,
                "X-BAPI-SIGN": signature,
                "Content-Type": "application/json"
            }

            url = self.base_url + endpoint

            if method == "GET":
                resp = requests.get(url, params=params, headers=headers, timeout=5)
            else:
                resp = requests.post(url, json=params, headers=headers, timeout=5)

            # JSON 안전 처리
            try:
                return resp.json()
            except Exception:
                return {
                    "success": False,
                    "error": "invalid_json_response",
                    "raw": resp.text
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
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

        return self._request(
            "POST",
            "/v5/order/create",
            {
                "category": "linear",
                "symbol": symbol,
                "side": side,
                "orderType": "Market",
                "qty": str(qty),
                "timeInForce": "GoodTillCancel",
                "leverage": str(leverage)
            }
        )


bybit_client = BybitClient()
