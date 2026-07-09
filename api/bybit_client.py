import time
import hmac
import hashlib
import requests


from config import (
    BYBIT_BASE_URL,
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
)



class BybitClient:


    def __init__(self):


        self.base = BYBIT_BASE_URL

        self.api_key = BYBIT_API_KEY

        self.api_secret = BYBIT_API_SECRET



        print("==============================")
        print("[BYBIT CLIENT INIT]")
        print("BASE :", self.base)
        print("KEY :", self.api_key[:6])
        print("==============================")



    # ==================================
    # SIGN
    # ==================================

    def sign(
        self,
        params
    ):


        timestamp = str(
            int(
                time.time()*1000
            )
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
    # HEADER
    # ==================================

    def headers(
        self,
        timestamp,
        recv_window,
        signature
    ):


        return {


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



    # ==================================
    # GET REQUEST
    # ==================================

    def get(
        self,
        endpoint,
        params=None
    ):


        if params is None:

            params = {}



        timestamp, recv_window, signature = (

            self.sign(params)

        )



        headers = self.headers(

            timestamp,

            recv_window,

            signature

        )



        url = (

            self.base

            +

            endpoint

        )



        try:


            response = requests.get(

                url,

                headers=headers,

                params=params,

                timeout=10

            )


            data = response.json()


            print(
                "[BYBIT GET RESPONSE]",
                data
            )


            return data



        except Exception as e:


            print(
                "[BYBIT GET ERROR]",
                e
            )


            return None



    # ==================================
    # POST REQUEST
    # ==================================

    def post(
        self,
        endpoint,
        params
    ):


        timestamp, recv_window, signature = (

            self.sign(params)

        )



        headers = self.headers(

            timestamp,

            recv_window,

            signature

        )



        url = (

            self.base

            +

            endpoint

        )



        try:


            response = requests.post(

                url,

                headers=headers,

                json=params,

                timeout=10

            )


            data = response.json()



            print(
                "[BYBIT POST RESPONSE]",
                data
            )


            return data



        except Exception as e:


            print(
                "[BYBIT POST ERROR]",
                e
            )


            return None




    # ==================================
    # TIME TEST
    # ==================================

    def server_time(self):


        try:


            r = requests.get(

                self.base

                +

                "/v5/market/time",

                timeout=5

            )


            return r.json()



        except Exception as e:


            print(e)

            return None




bybit_client = BybitClient()
