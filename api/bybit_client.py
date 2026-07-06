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
    # REQUEST
    # =====================================================

    def _request(self, method, endpoint, params=None):

        if params is None:
            params = {}

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

        return resp.json()

    # =====================================================
    # PRICE
    # =====================================================

    def get_price(self, symbol):

        endpoint = "/v5/market/tickers"

        params = {"category": "linear", "symbol": symbol}

        return self._request("GET", endpoint, params)

    # =====================================================
    # BALANCE
    # =====================================================

    def get_balance(self):

        endpoint = "/v5/account/wallet-balance"

        params = {"accountType": "UNIFIED"}

        return self._request("GET", endpoint, params)

    # =====================================================
    # ORDER
    # =====================================================

    def place_order(self, symbol, side, qty, leverage=1):

        endpoint = "/v5/order/create"

        params = {
            "category": "linear",
            "symbol": symbol,
            "side": side,
            "orderType": "Market",
            "qty": str(qty),
            "timeInForce": "GoodTillCancel",
            "leverage": str(leverage)
        }

        return self._request("POST", endpoint, params)


# =====================================================
# SINGLETON
# =====================================================

bybit_client = BybitClient()
