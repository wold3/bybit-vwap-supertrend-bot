import time
import hmac
import hashlib
import requests

from config import (
    BYBIT_BASE_URL,
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    ACCOUNT_TYPE
)


class BybitWallet:

    def __init__(self):

        self.api_key = BYBIT_API_KEY
        self.api_secret = BYBIT_API_SECRET

        self.base_url = BYBIT_BASE_URL

        self.account_type = ACCOUNT_TYPE

        print("==============================")
        print("[WALLET INIT]")
        print("KEY:", self.api_key[:6])
        print("BASE:", self.base_url)
        print("ACCOUNT:", self.account_type)
        print("==============================")


    def _sign(self, params):

        timestamp = str(
            int(time.time() * 1000)
        )

        recv_window = "5000"


        param_string = "&".join(
            [
                f"{k}={params[k]}"
                for k in sorted(params)
            ]
        )


        origin = (
            timestamp
            + self.api_key
            + recv_window
            + param_string
        )


        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            origin.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()


        return (
            timestamp,
            recv_window,
            signature
        )


    def get_equity(self):

        try:

            endpoint = (
                "/v5/account/wallet-balance"
            )


            params = {
                "accountType":
                    self.account_type
            }


            timestamp, recv_window, sign = (
                self._sign(params)
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


            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=10
            )


            data = response.json()


            print("[BYBIT RESPONSE]")
            print(data)


            if data.get("retCode") != 0:

                return 0


            result = data.get(
                "result",
                {}
            )


            list_data = result.get(
                "list",
                []
            )


            if not list_data:
                return 0


            account = list_data[0]


            equity = account.get(
                "totalEquity",
                0
            )


            return float(equity)


        except Exception as e:

            print(
                "[WALLET ERROR]",
                e
            )

            return 0



wallet = BybitWallet()
