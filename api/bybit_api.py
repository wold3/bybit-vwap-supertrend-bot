# =====================================================
# api/bybit_api.py
# Bybit V5 REST API
# =====================================================

import time
import hmac
import hashlib
import json
import requests
from urllib.parse import urlencode



from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    CATEGORY,
    DEFAULT_SYMBOL,
    INTERVAL,
    LEVERAGE,
    LIVE
)





BASE_URL = "https://api.bybit.com"





class BybitAPI:



    def __init__(self):


        self.key = BYBIT_API_KEY

        self.secret = BYBIT_API_SECRET


        self.recv_window = "5000"



        print(

            "[BYBIT API READY]"

        )









    # =====================================================
    # SIGNATURE
    # =====================================================

    def sign(
        self,
        timestamp,
        query=""
    ):


        payload = (

            str(timestamp)

            +

            self.key

            +

            self.recv_window

            +

            query

        )



        return hmac.new(

            bytes(

                self.secret,

                "utf-8"

            ),

            bytes(

                payload,

                "utf-8"

            ),

            hashlib.sha256

        ).hexdigest()







    # =====================================================
    # REQUEST
    # =====================================================

    def request(
        self,
        method,
        endpoint,
        params=None
    ):


        timestamp = str(

            int(time.time()*1000)

        )



        headers = {

            "X-BAPI-API-KEY":

                self.key,


            "X-BAPI-TIMESTAMP":

                timestamp,


            "X-BAPI-RECV-WINDOW":

                self.recv_window,


            "Content-Type":

                "application/json"

        }





        if method == "GET":


            query = urlencode(

                params or {}

            )



            sign_payload = query




        else:



            body = json.dumps(

                params or {},

                separators=(

                    ",",

                    ":"

                )

            )


            sign_payload = body





        signature = self.sign(

            timestamp,

            sign_payload

        )



        headers[

            "X-BAPI-SIGN"

        ] = signature






        try:


            if method == "GET":


                r = requests.get(

                    BASE_URL + endpoint,

                    headers=headers,

                    params=params,

                    timeout=10

                )


            else:


                r = requests.post(

                    BASE_URL + endpoint,

                    headers=headers,

                    data=body,

                    timeout=10

                )





            data = r.json()



            if data.get(

                "retCode",

                0

            ) != 0:



                print(

                    "[BYBIT ERROR]",

                    data

                )



            return data





        except Exception as e:



            print(

                "[REQUEST ERROR]",

                e

            )


            return None










    # =====================================================
    # WALLET
    # =====================================================

    def get_wallet_balance(self):


        return self.request(

            "GET",

            "/v5/account/wallet-balance",

            {


            "accountType":

                "UNIFIED"


            }

        )









    # =====================================================
    # KLINE
    # =====================================================

    def get_kline(
        self
    ):


        data = self.request(

            "GET",

            "/v5/market/kline",

            {


            "category":

                CATEGORY,


            "symbol":

                DEFAULT_SYMBOL,


            "interval":

                INTERVAL,


            "limit":

                200


            }

        )



        try:


            return data[

                "result"

            ][

                "list"

            ]



        except:


            return []









    # =====================================================
    # LEVERAGE
    # =====================================================

    def set_leverage(self):


        result = self.request(

            "POST",

            "/v5/position/set-leverage",

            {


            "category":

                CATEGORY,


            "symbol":

                DEFAULT_SYMBOL,


            "buyLeverage":

                str(LEVERAGE),


            "sellLeverage":

                str(LEVERAGE)


            }

        )



        return result







    # =====================================================
    # ORDER
    # =====================================================

    def place_order(
        self,
        side,
        qty
    ):



        if not LIVE:



            print(

                "[TEST ORDER]",

                side,

                qty

            )


            return {


                "retCode":

                    0,


                "test":

                    True


            }





        return self.request(

            "POST",

            "/v5/order/create",

            {


            "category":

                CATEGORY,


            "symbol":

                DEFAULT_SYMBOL,


            "side":

                side,


            "orderType":

                "Market",


            "qty":

                str(qty)


            }

        )









# =====================================================
# SINGLETON
# =====================================================


bybit_api = BybitAPI()
