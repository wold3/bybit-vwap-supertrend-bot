import requests
import time


from config import (
    BYBIT_BASE_URL,
    DEFAULT_SYMBOL
)



class WSClient:


    def __init__(self):


        self.base = BYBIT_BASE_URL

        self.symbol = DEFAULT_SYMBOL



        print("==============================")
        print("[SERVICE WS CLIENT INIT]")
        print("BASE :", self.base)
        print("SYMBOL :", self.symbol)
        print("==============================")



    def get_kline(
        self,
        interval="1"
    ):


        endpoint = (
            "/v5/market/kline"
        )



        params = {


            "category":

                "linear",


            "symbol":

                self.symbol,


            "interval":

                interval,


            "limit":

                500

        }



        try:


            r = requests.get(

                self.base + endpoint,

                params=params,

                timeout=10

            )


            data = r.json()



            print(
                "[KLINE RESPONSE]",
                data.get("retCode")
            )



            return data



        except Exception as e:


            print(
                "[KLINE ERROR]",
                e
            )


            return None





ws_client_service = WSClient()
