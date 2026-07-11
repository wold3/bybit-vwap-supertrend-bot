# =====================================================
# api/bybit_api.py
# Bybit V5 API Manager
# Demo / Live Support
# =====================================================

import time
import hmac
import hashlib
import requests
import json



from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    LIVE,
    CATEGORY,
    DEFAULT_SYMBOL,
    INTERVAL
)





class BybitAPI:


    def __init__(self):


        if LIVE:

            self.base_url = (
                "https://api.bybit.com"
            )

            self.ws_url = (
                "wss://stream.bybit.com/v5/private"
            )


        else:

            self.base_url = (
                "https://api-demo.bybit.com"
            )

            self.ws_url = (
                "wss://stream-demo.bybit.com/v5/private"
            )



        print(

            "[BYBIT API READY]"

        )



        print(

            "[MODE]",

            "LIVE" if LIVE else "DEMO"

        )









    # =====================================================
    # SIGN
    # =====================================================


    def sign(
        self,
        timestamp,
        body=""
    ):


        recv_window = "5000"


        param = (

            str(timestamp)

            +

            BYBIT_API_KEY

            +

            recv_window

            +

            body

        )



        return hmac.new(

            BYBIT_API_SECRET.encode(),

            param.encode(),

            hashlib.sha256

        ).hexdigest()







    # =====================================================
    # REQUEST
    # =====================================================


    def request(
        self,
        method,
        path,
        params=None
    ):


        try:


            timestamp = str(

                int(

                    time.time()*1000

                )

            )



            body = ""



            if method == "POST":


                body = json.dumps(

                    params

                )





            headers = {


                "X-BAPI-API-KEY":

                    BYBIT_API_KEY,


                "X-BAPI-TIMESTAMP":

                    timestamp,


                "X-BAPI-SIGN":

                    self.sign(

                        timestamp,

                        body

                    ),


                "X-BAPI-RECV-WINDOW":

                    "5000",


                "Content-Type":

                    "application/json"

            }







            url = (

                self.base_url

                +

                path

            )





            if method == "GET":


                r = requests.get(

                    url,

                    headers=headers,

                    params=params,

                    timeout=10

                )


            else:


                r = requests.post(

                    url,

                    headers=headers,

                    data=body,

                    timeout=10

                )





            data = r.json()



            print(

                "[BYBIT STATUS]",

                r.status_code

            )



            if data.get("retCode") != 0:


                print(

                    "[BYBIT ERROR]",

                    data

                )



            return data






        except Exception as e:


            print(

                "[BYBIT REQUEST ERROR]",

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


    def get_kline(self):


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



        if not data:


            return []



        try:


            return (

                data

                ["result"]

                ["list"]

            )



        except:


            return []









    # =====================================================
    # POSITION
    # =====================================================


    def get_position(self):


        return self.request(

            "GET",

            "/v5/position/list",

            {


                "category":

                    CATEGORY,


                "symbol":

                    DEFAULT_SYMBOL

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

                    str(qty),


                "timeInForce":

                    "IOC"

            }

        )









    # =====================================================
    # TP SL
    # =====================================================


    def set_trading_stop(
        self,
        tp,
        sl
    ):


        return self.request(

            "POST",

            "/v5/position/trading-stop",

            {


                "category":

                    CATEGORY,


                "symbol":

                    DEFAULT_SYMBOL,


                "takeProfit":

                    str(tp),


                "stopLoss":

                    str(sl),


                "tpslMode":

                    "Full"

            }

        )









# =====================================================
# INSTANCE
# =====================================================


bybit_api = BybitAPI()
