import time
import hmac
import hashlib
import json
import requests


from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    BYBIT_BASE_URL,
    DEFAULT_SYMBOL,
    LIVE_TRADING
)



class OrderManager:


    def __init__(self):

        self.base_url = BYBIT_BASE_URL
        self.symbol = DEFAULT_SYMBOL
        self.live = LIVE_TRADING


        print("==============================")
        print("[ORDER MANAGER INIT]")
        print("BASE :", self.base_url)
        print("LIVE :", self.live)
        print("SYMBOL :", self.symbol)
        print("==============================")



    # ==================================
    # SIGN
    # ==================================

    def _sign(
        self,
        payload
    ):

        timestamp = str(
            int(time.time() * 1000)
        )

        recv_window = "5000"


        origin = (
            timestamp
            +
            BYBIT_API_KEY
            +
            recv_window
            +
            payload
        )


        signature = hmac.new(

            BYBIT_API_SECRET.encode(),

            origin.encode(),

            hashlib.sha256

        ).hexdigest()


        return (
            timestamp,
            recv_window,
            signature
        )



    # ==================================
    # ORDER CREATE
    # ==================================

    def create_order(
        self,
        side="Buy",
        qty="0.001",
        order_type="Market"
    ):


        endpoint = "/v5/order/create"


        body = {

            "category": "linear",

            "symbol": self.symbol,

            "side": side,

            "positionIdx": 0,

            "orderType": order_type,

            "qty": str(qty)

        }


        payload = json.dumps(
            body,
            separators=(
                ",",
                ":"
            )
        )


        ts, recv, sign = self._sign(
            payload
        )


        headers = {


            "X-BAPI-API-KEY":

            BYBIT_API_KEY,


            "X-BAPI-TIMESTAMP":

            ts,


            "X-BAPI-RECV-WINDOW":

            recv,


            "X-BAPI-SIGN":

            sign,


            "Content-Type":

            "application/json"

        }



        url = (
            self.base_url
            +
            endpoint
        )



        print("==============================")
        print("[ORDER REQUEST]")
        print(url)
        print(body)
        print("==============================")



        if not self.live:


            print(
                "[DEMO ORDER MODE]"
            )



        response = requests.post(

            url,

            headers=headers,

            data=payload,

            timeout=10

        )


        result = response.json()


        print(
            "[ORDER RESPONSE]",
            result
        )



        return result





# singleton

order_manager = OrderManager()
