import requests
from config import BYBIT_TESTNET


class Bybit:

    def __init__(self):
        self.base = "https://api-testnet.bybit.com" if BYBIT_TESTNET else "https://api.bybit.com"

    def order(self, symbol, side, qty):

        return requests.post(
            self.base + "/v5/order/create",
            json={
                "category": "linear",
                "symbol": symbol,
                "side": side,
                "orderType": "Market",
                "qty": str(qty)
            }
        ).json()

    def position(self, symbol):

        return requests.get(
            self.base + "/v5/position/list",
            params={"category": "linear", "symbol": symbol}
        ).json()


bybit = Bybit()
