# =====================================================
# api/bybit_api.py
# Bybit V5 REST API Manager
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

        self.api_key = BYBIT_API_KEY

        self.api_secret = BYBIT_API_SECRET

        self.recv_window = "5000"


        print(
            "[BYBIT API READY]"
        )





    # =====================================================
    # SIGN
    # =====================================================

    def generate_signature(
        self,
        timestamp,
        payload
    ):


        origin = (

            str(timestamp)

            +

            self.api_key

            +

            self.recv_window

            +

            payload

        )


        return hmac.new(

            self.api_secret.encode(
                "utf-8"
            ),

            origin.encode(
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

            int(
                time.time() * 1000
            )

        )



        headers = {

            "X-BAPI-API-KEY":

                self.api_key,


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


            payload = query


            body = None




        else:



            body = json.dumps(

                params or {},

                separators=(

                    ",",

                    ":"

                )

            )


            payload = body







        signature = self.generate_signature(

            timestamp,

            payload

        )



        headers[

            "X-BAPI-SIGN"

        ] = signature





        try:



            if method == "GET":


                response = requests.get(

                    BASE_URL + endpoint,

                    params=params,

                    headers=headers,

                    timeout=10

                )



            else:


                response = requests.post(

                    BASE_URL + endpoint,

                    data=body,

                    headers=headers,

                    timeout=10

                )







            print(

                "[BYBIT STATUS]",

                response.status_code

            )



            try:


                data = response.json()



            except Exception:


                print(

                    "[BYBIT RAW]",

                    response.text[:500]

                )


                return None





            if data.get(

                "retCode"

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

    def get_wallet_balance(
        self
    ):


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


        result = self.request(

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


            return result[

                "result"

            ][

                "list"

            ]



        except Exception:



            return []









    # =====================================================
    # LEVERAGE
    # =====================================================

    def set_leverage(
        self
    ):


        return self.request(

            "POST",

            "/v5/position/set-leverage",

            {


                "category":

                    CATEGORY,


                "symbol":

                    DEFAULT_SYMBOL,


                "buyLeverage":

                    str(
                        LEVERAGE
                    ),


                "sellLeverage":

                    str(
                        LEVERAGE
                    )

            }

        )









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


                "mode":

                    "TEST"

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
