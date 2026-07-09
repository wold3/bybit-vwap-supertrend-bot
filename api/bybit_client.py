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
        print("KEY :", self.api_key[:6])
        print("==============================")



    # =====================================================
    # TIME
    # =====================================================

    def timestamp(self):

        return str(
            int(time.time() * 1000)
        )



    # =====================================================
    # SIGN
    # =====================================================

    def generate_signature(
        self,
        timestamp,
        query_string=""
    ):


        payload = (

            timestamp

            +

            self.api_key

            +

            self.recv_window

            +

            query_string

        )


        return hmac.new(

            self.api_secret.encode(
                "utf-8"
            ),

            payload.encode(
                "utf-8"
            ),

            hashlib.sha256

        ).hexdigest()



    # =====================================================
    # QUERY BUILDER
    # =====================================================

    def build_query(
        self,
        params
    ):


        if not params:

            return ""


        items = sorted(
            params.items()
        )


        return "&".join(

            f"{k}={v}"

            for k, v in items

        )



    # =====================================================
    # HEADERS
    # =====================================================

    def headers(
        self,
        signature,
        timestamp
    ):


        return {


            "X-BAPI-API-KEY":

                self.api_key,


            "X-BAPI-SIGN":

                signature,


            "X-BAPI-TIMESTAMP":

                timestamp,


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



        try:

            timestamp = self.timestamp()


            query = self.build_query(
                params
            )


            signature = self.generate_signature(
                timestamp,
                query
            )


            response = requests.get(

                self.base + endpoint,

                params=params,

                headers=self.headers(
                    signature,
                    timestamp
                ),

                timeout=10

            )


            data = response.json()


            print(
                "[BYBIT RESPONSE]",
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


        try:


            timestamp = self.timestamp()


            body = json.dumps(
                params,
                separators=(
                    ",",
                    ":"
                )
            )


            signature = self.generate_signature(
                timestamp,
                body
            )


            response = requests.post(

                self.base + endpoint,

                data=body,

                headers=self.headers(
                    signature,
                    timestamp
                ),

                timeout=10

            )



            data = response.json()



            print(
                "[BYBIT RESPONSE]",
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

            response = requests.get(

                self.base
                +
                "/v5/market/time",

                timeout=5

            )


            return response.json()



        except Exception as e:


            print(
                "[SERVER TIME ERROR]",
                e
            )


            return None



    # =====================================================
    # SUCCESS CHECK
    # =====================================================

    def is_success(
        self,
        response
    ):


        return (

            response is not None

            and

            response.get(
                "retCode"
            )

            ==

            0

        )




bybit_client = BybitClient()
