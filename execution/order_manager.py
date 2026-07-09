import time
import hmac
import hashlib
import requests

from config import (
    BYBIT_BASE_URL,
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    DEFAULT_SYMBOL,
    LIVE_TRADING,
)


class OrderManager:

    def __init__(self):

        self.base_url = BYBIT_BASE_URL

        self.api_key = BYBIT_API_KEY
        self.api_secret = BYBIT_API_SECRET

        self.symbol = DEFAULT_SYMBOL

        self.live = LIVE_TRADING


        print("==============================")
        print("[ORDER MANAGER INIT]")
        print("BASE :", self.base_url)
        print("LIVE :", self.live)
        print("SYMBOL :", self.symbol)
        print("==============================")


    def _sign(self, params):

        timestamp = str(
            int(time.time() * 1000)
        )

        recv_window = "5000"


        query = "&".join(
            [
                f"{k}={params[k]}"
                for k in sorted(params)
            ]
        )


        origin = (
            timestamp
            +
            self.api_key
            +
            recv_window
            +
            query
        )


        sign = hmac.new(
            self.api_secret.encode(),
            origin.encode(),
            hashlib.sha256
        ).hexdigest()


        return (
            timestamp,
            recv_window,
            sign
        )


    def _headers(self, timestamp, recv_window, sign):

        return {

            "X-BAPI-API-KEY":
                self.api_key,

            "X-BAPI-SIGN":
                sign,

            "X-BAPI-TIMESTAMP":
                timestamp,

            "X-BAPI-RECV-WINDOW":
                recv_window,

            "Content-Type":
                "application/json"
        }



    def place_order(
        self,
        side,
        qty,
        order_type="Market"
    ):


        if not self.live:

            print(
                "[ORDER BLOCKED] LIVE_TRADING=False"
            )

            return None



        endpoint = (
            "/v5/order/create"
        )


        params = {

            "category":
                "linear",

            "symbol":
                self.symbol,

            "side":
                side,

            "orderType":
                order_type,

            "qty":
                str(qty),

        }


        timestamp, recv_window, sign = (
            self._sign(params)
        )


        headers = self._headers(
            timestamp,
            recv_window,
            sign
        )


        url = (
            self.base_url
            +
            endpoint
        )


        try:

            print("[ORDER REQUEST]")
            print(url)
            print(params)


            r = requests.post(
                url,
                headers=headers,
                json=params,
                timeout=10
            )


            data = r.json()


            print("[ORDER RESPONSE]")
            print(data)


            return data



        except Exception as e:

            print(
                "[ORDER ERROR]",
                e
            )

            return None



    def cancel_order(
        self,
        order_id
    ):


        endpoint = (
            "/v5/order/cancel"
        )


        params = {

            "category":
                "linear",

            "symbol":
                self.symbol,

            "orderId":
                order_id

        }


        timestamp, recv_window, sign = (
            self._sign(params)
        )


        headers = self._headers(
            timestamp,
            recv_window,
            sign
        )


        try:

            r = requests.post(
                self.base_url + endpoint,
                headers=headers,
                json=params,
                timeout=10
            )


            data = r.json()

            print("[CANCEL RESPONSE]")
            print(data)

            return data


        except Exception as e:

            print(
                "[CANCEL ERROR]",
                e
            )

            return None



    def get_open_orders(self):


        endpoint = (
            "/v5/order/realtime"
        )


        params = {

            "category":
                "linear",

            "symbol":
                self.symbol

        }


        timestamp, recv_window, sign = (
            self._sign(params)
        )


        headers = self._headers(
            timestamp,
            recv_window,
            sign
        )


        try:

            r = requests.get(
                self.base_url + endpoint,
                headers=headers,
                params=params,
                timeout=10
            )


            data = r.json()

            print("[OPEN ORDERS]")
            print(data)

            return data


        except Exception as e:

            print(
                "[OPEN ORDER ERROR]",
                e
            )

            return None



order_manager = OrderManager()
