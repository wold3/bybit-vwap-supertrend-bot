import os
import time
import hmac
import hashlib
import requests

from pathlib import Path
from dotenv import load_dotenv



# =====================================
# LOAD ENV
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_PATH
)




class BybitWallet:


    def __init__(self):


        self.api_key = os.getenv(
            "BYBIT_API_KEY"
        )


        self.api_secret = os.getenv(
            "BYBIT_API_SECRET"
        )


        self.base_url = os.getenv(
            "BYBIT_BASE_URL",
            "https://api.bybit.com"
        )


        print(
            "[WALLET INIT] KEY:",
            self.api_key[:6]
            if self.api_key
            else "NONE"
        )



    def _sign(self, params):


        query = "&".join(

            [
                f"{k}={params[k]}"
                for k in sorted(params)
            ]

        )


        return hmac.new(

            self.api_secret.encode(),

            query.encode(),

            hashlib.sha256

        ).hexdigest()



    def get_equity(self):


        endpoint = (
            "/v5/account/wallet-balance"
        )


        timestamp = str(
            int(
                time.time()*1000
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



        try:


            r = requests.get(

                self.base_url + endpoint,

                params=params,

                timeout=5

            )


            data = r.json()



            if data.get("retCode") != 0:


                print(
                    "[BYBIT WALLET ERROR]",
                    data
                )

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
