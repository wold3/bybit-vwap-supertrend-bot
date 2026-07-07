import os
import time
import hmac
import hashlib
import requests


class BybitWallet:

    def __init__(self):

        self.api_key = os.getenv("BYBIT_API_KEY")
        self.api_secret = os.getenv("BYBIT_API_SECRET")

        self.base_url = os.getenv(
            "BYBIT_BASE_URL",
            "https://api.bybit.com"
        )


    # ============================================
    # WALLET BALANCE
    # ============================================
    def get_equity(self):

        endpoint = "/v5/account/wallet-balance"

        url = self.base_url + endpoint


        timestamp = str(
            int(time.time() * 1000)
        )


        params = {
            "accountType": "UNIFIED",
            "api_key": self.api_key,
            "timestamp": timestamp,
            "recv_window": "5000"
        }


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


        params["sign"] = signature


        try:

            res = requests.get(
                url,
                params=params,
                timeout=5
            )


            data = res.json()


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
                account["totalEquity"]
            )


            return equity


        except Exception as e:

            print(
                "[WALLET ERROR]",
                e
            )

            return 0



wallet = BybitWallet()
