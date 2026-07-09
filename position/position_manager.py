import time
import hmac
import hashlib
import requests


from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    BYBIT_BASE_URL,
    DEFAULT_SYMBOL
)



class PositionManager:


    def __init__(self):

        self.base_url = BYBIT_BASE_URL
        self.symbol = DEFAULT_SYMBOL

        self.position = None


        print("==============================")
        print("[POSITION MANAGER INIT]")
        print("BASE :", self.base_url)
        print("SYMBOL :", self.symbol)
        print("==============================")



    def _sign(self, query):

        ts = str(
            int(time.time()*1000)
        )

        recv = "5000"


        origin = (
            ts
            +
            BYBIT_API_KEY
            +
            recv
            +
            query
        )


        sign = hmac.new(

            BYBIT_API_SECRET.encode(),

            origin.encode(),

            hashlib.sha256

        ).hexdigest()


        return ts, recv, sign



    def get_position(self):


        endpoint = "/v5/position/list"


        query = (
            "category=linear"
            +
            "&symbol="
            +
            self.symbol
        )


        ts, recv, sign = self._sign(query)



        headers = {

            "X-BAPI-API-KEY":
            BYBIT_API_KEY,

            "X-BAPI-TIMESTAMP":
            ts,

            "X-BAPI-RECV-WINDOW":
            recv,

            "X-BAPI-SIGN":
            sign

        }



        url = (
            self.base_url
            +
            endpoint
            +
            "?"
            +
            query
        )


        try:


            r = requests.get(

                url,

                headers=headers,

                timeout=10

            )


            data = r.json()


            print(
                "[POSITION RESPONSE]",
                data
            )



            if data.get("retCode") == 0:


                self.position = (

                    data["result"]
                    ["list"]

                )


            return self.position



        except Exception as e:


            print(
                "[POSITION ERROR]",
                e
            )


            return None





position_manager = PositionManager()
