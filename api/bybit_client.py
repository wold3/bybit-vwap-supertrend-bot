import time
import hmac
import hashlib
import json
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


        self.recv_window = "5000"



        print("==============================")
        print("[BYBIT CLIENT INIT]")
        print("BASE :", self.base)


        if self.api_key:

            print(
                "KEY :",
                self.api_key[:6]
            )

        else:

            print(
                "KEY : NONE"
            )


        print("==============================")




    # =====================================================
    # SIGN
    # =====================================================

    def sign(
        self,
        timestamp,
        payload
    ):


        origin = (

            str(timestamp)

            +

            self.api_key

            +

            self.recv_window

            +

            payload

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





    # =====================================================
    # HEADER
    # =====================================================

    def headers(
        self,
        timestamp,
        signature
    ):


        return {


            "X-BAPI-API-KEY":

            self.api_key,



            "X-BAPI-SIGN":

            signature,



            "X-BAPI-TIMESTAMP":

            str(timestamp),



            "X-BAPI-RECV-WINDOW":

            self.recv_window,



            "Content-Type":

            "application/json"

        }





    # =====================================================
    # GET
    # =====================================================

    def get(
        self,
        endpoint,
        params=None
    ):


        if params is None:

            params = {}



        timestamp = int(

            time.time()*1000

        )



        query = "&".join(

            [

                f"{k}={params[k]}"

                for k in sorted(params)

            ]

        )



        signature = self.sign(

            timestamp,

            query

        )



        headers = self.headers(

            timestamp,

            signature

        )



        url = self.base + endpoint



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






    # =====================================================
    # POST
    # =====================================================

    def post(
        self,
        endpoint,
        params
    ):



        timestamp = int(

            time.time()*1000

        )




        body = json.dumps(

            params,

            separators=(
                ",",
                ":"
            )

        )





        signature = self.sign(

            timestamp,

            body

        )





        headers = self.headers(

            timestamp,

            signature

        )





        url = self.base + endpoint





        try:



            response = requests.post(

                url,

                headers=headers,

                data=body,

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







    # =====================================================
    # SERVER TIME
    # =====================================================

    def server_time(self):


        try:


            r = requests.get(

                self.base +

                "/v5/market/time",

                timeout=5

            )


            return r.json()



        except Exception as e:


            print(
                "[SERVER TIME ERROR]",
                e
            )


            return None






bybit_client = BybitClient()
