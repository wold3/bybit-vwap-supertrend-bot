import time
import hmac
import hashlib
import json
import requests


from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    BYBIT_BASE_URL,
)





class BybitClient:


    def __init__(self):


        self.key = BYBIT_API_KEY

        self.secret = BYBIT_API_SECRET

        self.base = BYBIT_BASE_URL



        print("==============================")
        print("[BYBIT CLIENT INIT]")
        print("BASE :", self.base)
        print("KEY :", self.key[:6])
        print("==============================")






    # =====================================================
    # SIGN
    # =====================================================

    def _sign(
        self,
        timestamp,
        recv_window,
        body
    ):


        payload = (

            str(timestamp)

            +

            self.key

            +

            str(recv_window)

            +

            body

        )



        return hmac.new(

            self.secret.encode(
                "utf-8"
            ),

            payload.encode(
                "utf-8"
            ),

            hashlib.sha256

        ).hexdigest()








    # =====================================================
    # HEADERS
    # =====================================================

    def _headers(
        self,
        body=""
    ):


        timestamp = str(

            int(
                time.time()*1000
            )

        )


        recv_window = "5000"



        sign = self._sign(

            timestamp,

            recv_window,

            body

        )



        return {


            "X-BAPI-API-KEY":

                self.key,


            "X-BAPI-SIGN":

                sign,


            "X-BAPI-TIMESTAMP":

                timestamp,


            "X-BAPI-RECV-WINDOW":

                recv_window,


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


        try:


            if params is None:

                params = {}



            query = ""


            if params:


                query = "&".join(

                    f"{k}={v}"

                    for k,v in params.items()

                )



            url = (

                self.base

                +

                endpoint

            )



            if query:


                url += "?" + query






            headers = self._headers(
                ""
            )



            response = requests.get(

                url,

                headers=headers,

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


            body = json.dumps(

                params,

                separators=(
                    ",",
                    ":"
                )

            )



            url = (

                self.base

                +

                endpoint

            )



            headers = self._headers(

                body

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
