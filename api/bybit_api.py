# =====================================================
# api/bybit_api.py
# Bybit V5 API Manager
# Demo / Live Trading
# =====================================================

import time
import hmac
import hashlib
import requests
import json


from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    CATEGORY,
    DEFAULT_SYMBOL,
    LIVE
)





class BybitAPI:


    def __init__(self):


        if LIVE:


            self.base_url = (
                "https://api.bybit.com"
            )


        else:


            # Bybit Demo Trading API

            self.base_url = (
                "https://api-demo.bybit.com"
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
        payload
    ):


        timestamp = str(

            int(

                time.time()*1000

            )

        )



        recv_window = "5000"



        param = (

            timestamp

            +

            BYBIT_API_KEY

            +

            recv_window

            +

            payload

        )



        signature = hmac.new(

            BYBIT_API_SECRET.encode(),

            param.encode(),

            hashlib.sha256

        ).hexdigest()



        return (

            timestamp,

            recv_window,

            signature

        )









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


            if params is None:

                params = {}



            if method == "GET":


                payload = (

                    json.dumps(

                        params,

                        separators=(
                            ",",
                            ":"
                        )

                    )

                )

            else:


                payload = json.dumps(

                    params,

                    separators=(
                        ",",
                        ":"
                    )

                )




            timestamp, recv, signature = self.sign(

                payload

            )



            headers = {


                "X-BAPI-API-KEY":

                    BYBIT_API_KEY,


                "X-BAPI-SIGN":

                    signature,


                "X-BAPI-TIMESTAMP":

                    timestamp,


                "X-BAPI-RECV-WINDOW":

                    recv,


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

                    json=params,

                    timeout=10

                )






            print(

                "[BYBIT STATUS]",

                r.status_code

            )



            data = r.json()



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
        self,
        limit=200
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

                    "5",


                "limit":

                    limit

            }

        )



        if not result:


            return []





        try:


            return (

                result

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

                    str(sl)

            }

        )









# =====================================================
# INSTANCE
# =====================================================


bybit_api = BybitAPI()
