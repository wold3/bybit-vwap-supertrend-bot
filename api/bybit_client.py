# api/bybit_client.py

import time
import hmac
import hashlib
import requests


from config import (
    BYBIT_BASE_URL,
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    ACCOUNT_TYPE
)



class BybitClient:


    def __init__(self):


        self.base_url = BYBIT_BASE_URL


        self.api_key = BYBIT_API_KEY


        self.api_secret = BYBIT_API_SECRET


        self.account_type = ACCOUNT_TYPE



        print("==============================")
        print("[BYBIT CLIENT INIT]")
        print("BASE :", self.base_url)
        print(
            "KEY :",
            self.api_key[:6]
            if self.api_key
            else None
        )
        print("==============================")



    # =====================================
    # SIGN
    # =====================================

    def sign(
        self,
        timestamp,
        recv_window,
        params
    ):


        param_str = params



        origin = (

            str(timestamp)

            +

            self.api_key

            +

            str(recv_window)

            +

            param_str

        )



        signature = hmac.new(

            self.api_secret.encode(
                "utf-8"
            ),

            origin.encode(
                "utf-8"
            ),

            hashlib.sha256

        ).hexdigest()



        return signature



    # =====================================
    # PRIVATE REQUEST
    # =====================================

    def private_request(
        self,
        method,
        endpoint,
        params=None
    ):


        if params is None:

            params = {}



        timestamp = str(
            int(
                time.time() * 1000
            )
        )


        recv_window = "5000"



        if method.upper() == "GET":


            query = "&".join(

                [
                    f"{k}={v}"
                    for k, v in sorted(params.items())
                ]

            )


            sign_payload = query



        else:


            import json


            sign_payload = json.dumps(

                params,

                separators=(
                    ",",
                    ":"
                )

            )



        signature = self.sign(

            timestamp,

            recv_window,

            sign_payload

        )



        headers = {


            "X-BAPI-API-KEY":

                self.api_key,


            "X-BAPI-SIGN":

                signature,


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
            "[REQUEST]",
            method,
            url
        )



        if method.upper() == "GET":


            response = requests.get(

                url,

                headers=headers,

                params=params,

                timeout=10

            )



        else:


            response = requests.post(

                url,

                headers=headers,

                json=params,

                timeout=10

            )



        data = response.json()



        print(
            "[BYBIT RESPONSE]",
            data
        )



        return data




    # =====================================
    # SERVER TIME
    # =====================================

    def server_time(
        self
    ):


        url = (

            self.base_url

            +

            "/v5/market/time"

        )



        return requests.get(
            url,
            timeout=10
        ).json()





bybit_client = BybitClient()
