import time
import hmac
import hashlib
import requests
import json
import logging

from config import BYBIT_API_KEY, BYBIT_API_SECRET, BYBIT_TESTNET

logger = logging.getLogger(__name__)


class BybitClient:

    def __init__(self):

        self.api_key = BYBIT_API_KEY
        self.api_secret = BYBIT_API_SECRET

        if BYBIT_TESTNET:
            self.base_url = "https://api-testnet.bybit.com"
        else:
            self.base_url = "https://api.bybit.com"

    # =====================================================
    # SIGNATURE (FIXED)
    # =====================================================
    def _sign(self, params: dict):

        timestamp = str(int(time.time() * 1000))

        # 🔥 FIX: sort_keys 중요 (서명 안정화)
        param_str = (
            timestamp +
            self.api_key +
            json.dumps(params, separators=(',', ':'), sort_keys=True)
        )

        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            param_str.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        return timestamp, signature

    # =====================================================
    # REQUEST (SAFE)
    # =====================================================
    def _request(self, method, endpoint, params=None):

        try:
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

            # 🔥 FIX: JSON 안전 처리
            try:
                data = resp.json()
            except Exception:
                logger.error(f"Invalid JSON response: {resp.text}")
                return {}

            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP error: {e}")
            return {}

        except Exception as e:
            logger.error(f"Request error: {e}")
            return {}

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
