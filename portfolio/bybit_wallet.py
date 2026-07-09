import os
import time
import hmac
import hashlib
import requests

from urllib.parse import urlencode
from dotenv import load_dotenv


# =====================================
# ENV LOAD
# =====================================

load_dotenv()


# =====================================
# CONFIG
# =====================================

API_KEY = os.getenv(
    "BYBIT_API_KEY"
)

API_SECRET = os.getenv(
    "BYBIT_API_SECRET"
)

BASE_URL = os.getenv(
    "BYBIT_BASE_URL",
    "https://api.bybit.com"
)

ACCOUNT_TYPE = os.getenv(
    "ACCOUNT_TYPE",
    "UNIFIED"
)


# =====================================
# WALLET
# =====================================

class BybitWallet:


    def __init__(self):

        self.api_key = API_KEY

        self.api_secret = API_SECRET

        self.base_url = BASE_URL


        print("==============================")
        print("[WALLET INIT]")
        print(
            "KEY:",
            self.api_key[:6]
            if self.api_key
            else None
        )

        print(
            "BASE:",
            self.base_url
        )

        print("==============================")


    # =================================
    # SIGN
    # =================================

    def _sign(
        self,
        timestamp,
        recv_window,
        query_string
    ):


        origin = (
            timestamp
            +
            self.api_key
            +
            recv_window
            +
            query_string
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



    # =================================
    # REQUEST
    # =================================

    def _get(
        self,
        endpoint,
        params
    ):


        timestamp = str(
            int(
                time.time()*1000
            )
        )


        recv_window = "5000"


        query_string = urlencode(
            params
        )


        sign = self._sign(
            timestamp,
            recv_window,
            query_string
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


        try:


            response = requests.get(

                url,

                params=params,

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
                "[WALLET REQUEST ERROR]",
                e
            )


            return None



    # =================================
    # EQUITY
    # =================================

    def get_equity(self):


        params = {

            "accountType":
                ACCOUNT_TYPE

        }


        result = self._get(

            "/v5/account/wallet-balance",

            params

        )


        if not result:

            return 0



        if result.get(
            "retCode"
        ) != 0:


            return 0



        try:


            account = (
                result
                ["result"]
                ["list"]
                [0]
            )


            equity = float(
                account["totalEquity"]
            )


            print(
                "[ACCOUNT EQUITY]",
                equity
            )


            return equity



        except Exception as e:


            print(
                "[EQUITY PARSE ERROR]",
                e
            )


            return 0



# =====================================
# INSTANCE
# =====================================

wallet = BybitWallet()
