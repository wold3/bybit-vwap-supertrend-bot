import os
import time
import hmac
import hashlib
import requests

from dotenv import load_dotenv


load_dotenv()


class BybitWallet:


    def __init__(self):

        self.api_key = (
            os.getenv("BYBIT_API_KEY", "")
            .strip()
        )


        self.api_secret = (
            os.getenv("BYBIT_API_SECRET", "")
            .strip()
        )


        self.base_url = (
            os.getenv(
                "BYBIT_BASE_URL",
                "https://api.bybit.com"
            )
            .strip()
        )


        print(
            "[WALLET INIT]"
        )

        print(
            "KEY:",
            self.api_key[:6]
            if self.api_key
            else None
        )

        print(
            "SECRET:",
            self.api_secret[:6]
            if self.api_secret
            else None
        )

        print(
            "BASE:",
            self.base_url
        )



    # ==================================
    # SIGN
    # ==================================

    def _sign(
        self,
        params
    ):


        query_string = "&".join(

            [
                f"{key}={params[key]}"
                for key in sorted(params)
            ]

        )


        signature = hmac.new(

            self.api_secret.encode(
                "utf-8"
            ),

            query_string.encode(
                "utf-8"
            ),

            hashlib.sha256

        ).hexdigest()



        print(
            "[SIGN STRING]",
            query_string
        )


        print(
            "[SIGN]",
            signature
        )


        return signature




    # ==================================
    # EQUITY
    # ==================================

    def get_equity(self):


        if not self.api_key:

            print(
                "[ERROR] API KEY EMPTY"
            )

            return 0



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
                time.time() * 1000
            )

        )



        params = {


            "accountType":
                "UNIFIED",


            "api_key":
                self.api_key,


            "timestamp":
                timestamp,


            "recv_window":
                "5000"


        }



        params["sign"] = self._sign(
            params
        )



        headers = {


            "X-BAPI-API-KEY":
                self.api_key,


            "X-BAPI-SIGN":
                params["sign"],


            "X-BAPI-TIMESTAMP":
                timestamp,


            "X-BAPI-RECV-WINDOW":
                "5000"


        }



        try:


            print(
                "[REQUEST URL]",
                url
            )


            print(
                "[REQUEST PARAMS]",
                params
            )



            response = requests.get(

                url,

                params=params,

                headers=headers,

                timeout=5

            )



            print(
                "[HTTP]",
                response.status_code
            )



            data = response.json()



            print(
                "[BYBIT RESPONSE]",
                data
            )



            if data.get(
                "retCode"
            ) != 0:


                return 0



            account = (
                data["result"]
                ["list"][0]
            )



            equity = float(

                account[
                    "totalEquity"
                ]

            )



            return equity



        except Exception as e:


            print(
                "[WALLET EXCEPTION]",
                e
            )


            return 0





wallet = BybitWallet()
