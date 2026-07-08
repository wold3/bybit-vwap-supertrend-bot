import os
import time
import hmac
import hashlib
import requests

from dotenv import load_dotenv


load_dotenv()



class BybitWallet:


    def __init__(self):


        self.api_key = os.getenv(
            "BYBIT_API_KEY",
            ""
        ).strip()


        self.api_secret = os.getenv(
            "BYBIT_API_SECRET",
            ""
        ).strip()


        self.base_url = os.getenv(
            "BYBIT_BASE_URL",
            "https://api.bybit.com"
        ).strip()



        print(
            "[WALLET INIT]"
        )

        print(
            "KEY:",
            self.api_key[:6]
        )



    # ==================================
    # BYBIT V5 SIGN
    # ==================================

    def create_signature(
        self,
        timestamp,
        recv_window,
        params
    ):


        query_string = "&".join(

            [
                f"{k}={params[k]}"
                for k in sorted(params)
            ]

        )


        origin_string = (

            timestamp

            +

            self.api_key

            +

            recv_window

            +

            query_string

        )



        print(
            "[ORIGIN STRING]",
            origin_string
        )



        signature = hmac.new(

            self.api_secret.encode(
                "utf-8"
            ),

            origin_string.encode(
                "utf-8"
            ),

            hashlib.sha256

        ).hexdigest()



        print(
            "[SIGN]",
            signature
        )


        return signature





    # ==================================
    # EQUITY
    # ==================================

    def get_equity(self):


        endpoint = (
            "/v5/account/wallet-balance"
        )


        url = (
            self.base_url
            +
            endpoint
        )



        timestamp = str(

            int(
                time.time()*1000
            )

        )


        recv_window = "5000"



        params = {


            "accountType":
                "UNIFIED"


        }



        sign = self.create_signature(

            timestamp,

            recv_window,

            params

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


        }



        try:


            r = requests.get(

                url,

                params=params,

                headers=headers,

                timeout=5

            )



            data = r.json()



            print(
                "[BYBIT RESPONSE]",
                data
            )



            if data.get(
                "retCode"
            ) != 0:


                return 0



            equity = float(

                data["result"]
                ["list"][0]
                ["totalEquity"]

            )


            return equity



        except Exception as e:


            print(
                "[WALLET ERROR]",
                e
            )


            return 0





wallet = BybitWallet()
