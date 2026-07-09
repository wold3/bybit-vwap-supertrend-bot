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


        self.base_url = BYBIT_BASE_URL

        self.api_key = BYBIT_API_KEY

        self.api_secret = BYBIT_API_SECRET


        self.account_type = ACCOUNT_TYPE



        print("==============================")
        print("[WALLET INIT]")
        print("KEY:", self.api_key[:6])
        print("BASE:", self.base_url)
        print("==============================")



    def sign(
        self,
        params
    ):


        timestamp = str(
            int(time.time()*1000)
        )


        recv_window = "5000"


        query = "&".join(

            [
                f"{k}={params[k]}"
                for k in sorted(params)
            ]

        )



        origin = (

            timestamp

            +

            self.api_key

            +

            recv_window

            +

            query

        )



        sign = hmac.new(

            self.api_secret.encode(),

            origin.encode(),

            hashlib.sha256

        ).hexdigest()



        return (
            timestamp,
            recv_window,
            sign
        )




    def get_equity(self):


        endpoint = (
            "/v5/account/wallet-balance"
        )


        params = {

            "accountType":
                self.account_type

        }



        timestamp, recv_window, sign = (

            self.sign(params)

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



        try:


            r = requests.get(

                self.base_url + endpoint,

                headers=headers,

                params=params,

                timeout=10

            )



            data = r.json()



            print(
                "[BYBIT RESPONSE]",
                data
            )



            if data.get("retCode") != 0:


                return 0



            account = (

                data["result"]
                ["list"]
                [0]

            )



            return float(

                account.get(
                    "totalEquity",
                    0
                )

            )



        except Exception as e:


            print(
                "[WALLET ERROR]",
                e
            )


            return 0





wallet = BybitWallet()
