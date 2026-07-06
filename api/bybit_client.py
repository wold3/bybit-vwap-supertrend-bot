import requests

from config import BYBIT_TESTNET


class BybitClient:

    def __init__(self):

        self.base_url = (
            "https://api-testnet.bybit.com"
            if BYBIT_TESTNET else
            "https://api.bybit.com"
        )

    def _request(self, method, endpoint, params=None):

        url = self.base_url + endpoint

        if method == "GET":
            resp = requests.get(url, params=params, timeout=5)
        else:
            resp = requests.post(url, json=params, timeout=5)

        return resp.json()

    def place_order(self, symbol, side, qty, leverage=1):

        endpoint = "/v5/order/create"

        params = {
            "category": "linear",
            "symbol": symbol,
            "side": side,
            "orderType": "Market",
            "qty": str(qty),
            "timeInForce": "GoodTillCancel"
        }

        return self._request("POST", endpoint, params)

    def get_positions(self, symbol):

        endpoint = "/v5/position/list"

        params = {
            "category": "linear",
            "symbol": symbol
        }

        return self._request("GET", endpoint, params)


bybit_client = BybitClient()
