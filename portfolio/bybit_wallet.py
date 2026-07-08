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
        )


        self.api_secret = os.getenv(
            "BYBIT_API_SECRET",
            ""
        )


        self.base_url = os.getenv(
            "BYBIT_BASE_URL",
            "https://api.bybit.com"
        )


        print(
            "[WALLET INIT]",
            "KEY:",
            self.api_key[:6] if self.api_key else "NONE"
        )



    # ============================================
    # SIGNATURE
    # ============================================

    def _generate_signature(
        self,
        params
    ):


        query = "&".join(

            [
                f"{k}={params[k]}"
                for k in sorted(params)
            ]

        )


        signature = hmac.new(

            self.api_secret.encode(),

            query.encode(),

            hashlib.sha256

        ).hexdigest()


        return signature




    # ============================================
    # WALLET BALANCE
    # ============================================

    def get_equity(self):


        if not self.api_key or not self.api_secret:


            print(
                "[WALLET ERROR] API KEY MISSING"
            )


            return 0




        endpoint = "/v5/account/wallet-balance"


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



        params["sign"] = self._generate_signature(

            params

        )



        try:



            response = requests.get(


                self.base_url + endpoint,


                params=params,


                timeout=5


            )



            data = response.json()



            if data.get("retCode") != 0:



                print(

                    "[BYBIT WALLET ERROR]",

                    data

                )


                return 0




            result = data.get(

                "result",

                {}

            )



            accounts = result.get(

                "list",

                []

            )



            if not accounts:



                print(

                    "[WALLET ERROR] EMPTY RESULT"

                )


                return 0




            equity = float(


                accounts[0]
                .get(
                    "totalEquity",
                    0
                )


            )



            return equity




        except requests.exceptions.Timeout:



            print(

                "[WALLET ERROR] TIMEOUT"

            )


            return 0




        except Exception as e:



            print(

                "[WALLET ERROR]",

                e

            )


            return 0




    # ============================================
    # AVAILABLE BALANCE
    # ============================================

    def get_available_balance(self):


        endpoint = "/v5/account/wallet-balance"


        equity = self.get_equity()


        return equity





# ============================================
# SINGLETON
# ============================================

wallet = BybitWallet()
