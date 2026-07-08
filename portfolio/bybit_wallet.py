import os
import time
import hmac
import hashlib
import requests


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
            self.api_key[:6] if self.api_key else None
        )



    # =====================================
    # SIGN
    # =====================================

    def _sign(self, params):


        query = "&".join(
            f"{k}={params[k]}"
            for k in sorted(params)
        )


        return hmac.new(
            self.api_secret.encode(),
            query.encode(),
            hashlib.sha256
        ).hexdigest()



    # =====================================
    # EQUITY
    # =====================================

    def get_equity(self):


        if not self.api_key or not self.api_secret:

            print(
                "[WALLET] API KEY NOT FOUND"
            )

            return 0



        endpoint = (
            "/v5/account/wallet-balance"
        )


        params = {


            "accountType":
                "UNIFIED",


            "api_key":
                self.api_key,


            "timestamp":
                str(
                    int(
                        time.time()*1000
                    )
                ),


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



            account = (
                data["result"]
                ["list"][0]
            )



            equity = float(

                account.get(
                    "totalEquity",
                    0
                )

            )



            return equity



        except Exception as e:


            print(
                "[WALLET EXCEPTION]",
                e
            )


            return 0





wallet = BybitWallet()
