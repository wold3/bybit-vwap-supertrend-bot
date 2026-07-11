# =====================================================
# api/bybit_api.py
# Bybit V5 API Manager
# =====================================================

import time
import hmac
import hashlib
import json
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
        payload
    ):


        return hmac.new(

            self.secret.encode(),

            payload.encode(),

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


        if params is None:

            params = {}



        timestamp = str(

            int(

                time.time()*1000

            )

        )


        recv_window = "5000"





        if method == "GET":


            query = "&".join(

                f"{k}={v}"

                for k,v in params.items()

            )


            payload = query



        else:


            payload = json.dumps(

                params,

                separators=(
                    ",",
                    ":"
                )

            )





        sign_string = (

            timestamp

            +

            self.key

            +

            recv_window

            +

            payload

        )



        signature = self.sign(

            sign_string

        )







        headers = {


            "X-BAPI-API-KEY":

                self.key,


            "X-BAPI-SIGN":

                signature,


            "X-BAPI-TIMESTAMP":

                timestamp,


            "X-BAPI-RECV-WINDOW":

                recv_window,


            "Content-Type":

                "application/json"

        }






        url = self.base + endpoint






        try:


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
    # SET TP SL
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
# INSTANCE
# =====================================================


bybit_api = BybitAPI()
