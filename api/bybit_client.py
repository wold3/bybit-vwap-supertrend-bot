import requests

from config import BYBIT_TESTNET


class BybitClient:

    def __init__(self):

        self.base_url = (
            "https://api-testnet.bybit.com"
            if BYBIT_TESTNET else
            "https://api.bybit.com"
        )

    def place_order(self, symbol, side, qty):

        return requests.post(
            self.base_url + "/v5/order/create",
            json={
                "category": "linear",
                "symbol": symbol,
                "side": side,
                "orderType": "Market",
                "qty": str(qty)
            }
        ).json()

    def get_positions(self, symbol):

        return requests.get(
            self.base_url + "/v5/position/list",
            params={
                "category": "linear",
                "symbol": symbol
            }
        ).json()


bybit_client = BybitClient()
