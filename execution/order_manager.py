import time
import hmac
import hashlib
import requests
import json


from config import (
    BYBIT_BASE_URL,
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    DEFAULT_SYMBOL,
    LIVE_TRADING
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



    # ==================================
    # SIGN
    # ==================================

    def sign(
        self,
        params
    ):


        timestamp = str(
            int(time.time()*1000)
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



        signature = hmac.new(

            self.api_secret.encode(),

            origin.encode(),

            hashlib.sha256

        ).hexdigest()



        return (
            timestamp,
            recv_window,
            signature
        )




    # ==================================
    # PLACE ORDER
    # ==================================

    def place_order(
        self,
        side,
        qty
    ):


        if not self.live:


            print(
                "[ORDER BLOCKED] LIVE_TRADING=False"
            )


            return None




        endpoint = (
            "/v5/order/create"
        )



        body = {


            "category":
                "linear",


            "symbol":
                self.symbol,


            "side":
                side,


            "orderType":
                "Market",


            "qty":
                str(qty),


            "timeInForce":
                "IOC"

        }




        timestamp, recv_window, sign = (

            self.sign(body)

        )



        headers = {


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



        url = (

            self.base_url

            +

            endpoint

        )



        print(
            "[ORDER REQUEST]",
            body
        )



        try:


            r = requests.post(

                url,

                headers=headers,

                json=body,

                timeout=10

            )



            data = r.json()



            print(
                "[ORDER RESPONSE]",
                data
            )



            return data



        except Exception as e:


            print(
                "[ORDER ERROR]",
                e
            )


            return None




    # ==================================
    # STRATEGY CONNECT
    # ==================================

    def execute(
        self,
        signal
    ):



        if signal == "BUY":


            return self.place_order(

                "Buy",

                0.001

            )



        elif signal == "SELL":


            return self.place_order(

                "Sell",

                0.001

            )



        return None





order_manager = OrderManager()
