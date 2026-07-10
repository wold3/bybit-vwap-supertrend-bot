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


        self.base_url = BYBIT_BASE_URL

        self.api_key = BYBIT_API_KEY

        self.api_secret = BYBIT_API_SECRET



        print("==============================")
        print("[BYBIT CLIENT INIT]")
        print("BASE :", self.base_url)
        print("KEY :", self.api_key[:6])
        print("==============================")









    # =====================================================
    # SIGN
    # =====================================================

    def _sign(
        self,
        timestamp,
        params
    ):


        recv_window = "5000"


        if isinstance(params, dict):

            param_str = json.dumps(
                params,
                separators=(",", ":")
            )

        else:

            param_str = str(params)



        payload = (

            str(timestamp)

            +

            self.api_key

            +

            recv_window

            +

            param_str

        )



        signature = hmac.new(

            self.api_secret.encode(),

            payload.encode(),

            hashlib.sha256

        ).hexdigest()



        return signature







    # =====================================================
    # HEADERS
    # =====================================================

    def _headers(
        self,
        params
    ):


        timestamp = str(
            int(time.time()*1000)
        )


        recv_window = "5000"



        sign = self._sign(

            timestamp,

            params

        )



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

                "application/json",

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


            query = params



            headers = self._headers(
                query
            )



            url = (

                self.base_url

                +

                endpoint

            )



            response = requests.get(

                url,

                headers=headers,

                params=query,

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
        params=None
    ):


        if params is None:

            params = {}




        try:



            body = json.dumps(

                params,

                separators=(",", ":")

            )



            headers = self._headers(

                params

            )



            url = (

                self.base_url

                +

                endpoint

            )




            response = requests.post(

                url,

                headers=headers,

                data=body,

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











bybit_client = BybitClient()
