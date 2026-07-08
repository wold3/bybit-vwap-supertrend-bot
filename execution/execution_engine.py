import os
import time
import hmac
import hashlib
import json
import requests

from dotenv import load_dotenv

from trade_db import trade_db
from risk.trailing_stop_manager import trailing_stop_manager
from position.position_manager import position_manager


load_dotenv()


class ExecutionEngine:


    def __init__(self):

        self.api_key = os.getenv(
            "BYBIT_API_KEY",
            ""
        )

        self.api_secret = os.getenv(
            "BYBIT_API_SECRET",
            ""
        )

        self.base_url = os.getenv(
            "BYBIT_BASE_URL",
            "https://api-testnet.bybit.com"
        )

        self.retry = int(
            os.getenv(
                "ORDER_RETRY",
                "3"
            )
        )


        # ==============================
        # TIME SYNC
        # ==============================

        self.recv_window = "10000"

        self.time_offset = 0

        self.sync_time()



    # =====================================
    # BYBIT SERVER TIME SYNC
    # =====================================

    def sync_time(self):

        try:

            response = requests.get(

                self.base_url
                +
                "/v5/market/time",

                timeout=5

            )


            data = response.json()


            server_time = int(
                data["time"]
            )


            local_time = int(
                time.time() * 1000
            )


            self.time_offset = (

                server_time

                -

                local_time

            )


            print(

                "[TIME SYNC]",

                self.time_offset,

                "ms"

            )


        except Exception as e:


            print(

                "[TIME SYNC ERROR]",

                e

            )

            self.time_offset = 0



    # =====================================
    # SIGN
    # =====================================

    def sign(
        self,
        timestamp,
        body
    ):


        payload = (

            timestamp

            +

            self.api_key

            +

            self.recv_window

            +

            body

        )


        return hmac.new(

            self.api_secret.encode(),

            payload.encode(),

            hashlib.sha256

        ).hexdigest()



    # =====================================
    # REQUEST
    # =====================================

    def request(
        self,
        url,
        body=None,
        method="POST"
    ):


        timestamp = str(

            int(
                time.time() * 1000
            )

            +

            self.time_offset

        )


        body = body or {}


        body_json = json.dumps(

            body,

            separators=(",", ":")

        )


        headers = {


            "Content-Type":

                "application/json",



            "X-BAPI-API-KEY":

                self.api_key,



            "X-BAPI-TIMESTAMP":

                timestamp,



            "X-BAPI-RECV-WINDOW":

                self.recv_window,



            "X-BAPI-SIGN":

                self.sign(

                    timestamp,

                    body_json

                    if method.upper()=="POST"

                    else ""

                )

        }



        try:


            if method.upper()=="GET":


                response = requests.get(

                    url,

                    params=body,

                    headers=headers,

                    timeout=10

                )


            else:


                response = requests.post(

                    url,

                    json=body,

                    headers=headers,

                    timeout=10

                )



            print("======================")

            print(
                "[BYBIT]",
                response.text
            )

            print("======================")


            return response.json()



        except Exception as e:


            print(

                "[REQUEST ERROR]",

                e

            )


            return {}



    # =====================================
    # ACCOUNT EQUITY
    # =====================================

    def get_account_equity(self):


        result = self.request(

            self.base_url

            +

            "/v5/account/wallet-balance",

            {

                "accountType":

                    "UNIFIED"

            },

            method="GET"

        )


        try:


            return float(

                result["result"]

                ["list"]

                [0]

                ["totalEquity"]

            )


        except:


            return 0.0



    # =====================================
    # WALLET
    # =====================================

    def get_wallet_balance(self):

        return self.get_account_equity()



    # =====================================
    # STATUS
    # =====================================

    def status(self):


        return {


            "api_key":

                bool(self.api_key),


            "base_url":

                self.base_url,


            "time_offset":

                self.time_offset,


            "recv_window":

                self.recv_window


        }





execution_engine = ExecutionEngine()
