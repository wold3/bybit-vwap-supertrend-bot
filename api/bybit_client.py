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


        if not self.api_key or not self.api_secret:

            raise Exception(
                "BYBIT API KEY / SECRET missing"
            )


        print("==============================")
        print("[BYBIT CLIENT INIT]")
        print("BASE :", self.base)
        print("KEY  :", self.api_key[:6])
        print("==============================")



    # ==================================
    # QUERY BUILDER
    # ==================================

    def build_query(
        self,
        params
    ):

        if not params:

            return ""


        return "&".join(

            [

                f"{k}={params[k]}"

                for k in sorted(params)

            ]

        )



    # ==================================
    # SIGN
    # ==================================

    def sign(
        self,
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


        query = self.build_query(

            params

        )


        payload = (

            timestamp

            +

            self.api_key

            +

            recv_window

            +

            query

        )


        signature = hmac.new(

            self.api_secret.encode(
                "utf-8"
            ),

            payload.encode(
                "utf-8"
            ),

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
    # GET
    # ==================================

    def get(
        self,
        endpoint,
        params=None
    ):


        if params is None:

            params = {}



        timestamp, recv_window, signature = (

            self.sign(
                params
            )

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
                "[BYBIT GET]",
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
    # POST
    # ==================================

    def post(
        self,
        endpoint,
        params
    ):


        timestamp, recv_window, signature = (

            self.sign(
                params
            )

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
                "[BYBIT POST]",
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
    # SERVER TIME
    # ==================================

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
                "[TIME ERROR]",
                e
            )


            return None



    # ==================================
    # WALLET BALANCE
    # ==================================

    def wallet_balance(self):


        return self.get(

            "/v5/account/wallet-balance",

            {

                "accountType":
                    "UNIFIED"

            }

        )



    # ==================================
    # POSITION
    # ==================================

    def position(
        self,
        symbol
    ):


        return self.get(

            "/v5/position/list",

            {

                "category":
                    "linear",

                "symbol":
                    symbol

            }

        )



    # ==================================
    # ORDER
    # ==================================

    def create_order(
        self,
        symbol,
        side,
        qty
    ):


        params = {


            "category":

                "linear",


            "symbol":

                symbol,


            "side":

                side,


            "orderType":

                "Market",


            "qty":

                str(qty)

        }



        return self.post(

            "/v5/order/create",

            params

        )



bybit_client = BybitClient()
