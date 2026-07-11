# =====================================================
# api/bybit_api.py
# Bybit V5 API Wrapper
# =====================================================

import time
import hmac
import hashlib
import requests


from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    BYBIT_BASE_URL,
    CATEGORY,
    DEFAULT_SYMBOL,
    INTERVAL,
    LEVERAGE
)





class BybitAPI:


    def __init__(self):


        self.key = BYBIT_API_KEY

        self.secret = BYBIT_API_SECRET


        self.base = BYBIT_BASE_URL



        print(
            "[BYBIT API READY]"
        )







    # =====================================================
    # SIGN
    # =====================================================


    def sign(
        self,
        timestamp,
        recv_window,
        body
    ):


        param = (

            str(timestamp)

            +

            self.key

            +

            str(recv_window)

            +

            body

        )



        return hmac.new(

            self.secret.encode(),

            param.encode(),

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


        recv_window = "5000"



        if method == "GET":


            body = ""


            url = (

                self.base

                +

                endpoint

            )


            response = requests.get(

                url,

                params=params,

                headers=self.headers(

                    timestamp,

                    recv_window,

                    body

                )

            )



        else:


            import json


            body = json.dumps(

                params

            )


            url = (

                self.base

                +

                endpoint

            )


            response = requests.post(

                url,

                data=body,

                headers=self.headers(

                    timestamp,

                    recv_window,

                    body

                )

            )



        try:


            data = response.json()


        except:


            print(

                "[BYBIT RAW]",

                response.text

            )


            return None




        print(

            "[BYBIT STATUS]",

            response.status_code

        )



        if data.get("retCode") != 0:


            print(

                "[BYBIT ERROR]",

                data

            )



        return data







    def headers(
        self,
        timestamp,
        recv_window,
        body
    ):


        return {


            "X-BAPI-API-KEY":

                self.key,


            "X-BAPI-TIMESTAMP":

                timestamp,


            "X-BAPI-RECV-WINDOW":

                recv_window,


            "X-BAPI-SIGN":

                self.sign(

                    timestamp,

                    recv_window,

                    body

                ),


            "Content-Type":

                "application/json"

        }









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
    # LEVERAGE
    # =====================================================


    def set_leverage(self):


        return self.request(

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
