# =====================================================
# api/bybit_api.py
# Bybit V5 API Client
# =====================================================

import time
import hmac
import hashlib
import json
import requests
import math



from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    BYBIT_BASE_URL,

    CATEGORY,
    DEFAULT_SYMBOL,

    LIVE
)





class BybitAPI:



    def __init__(self):


        self.api_key = BYBIT_API_KEY

        self.api_secret = BYBIT_API_SECRET

        self.base_url = BYBIT_BASE_URL


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

            self.api_secret.encode(),

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


        try:


            timestamp = str(

                int(time.time()*1000)

            )



            recv_window = "5000"



            if params:


                if method == "GET":


                    query = "&".join(

                        [

                            f"{k}={v}"

                            for k,v in params.items()

                        ]

                    )

                    payload = query



                else:


                    payload = json.dumps(

                        params,

                        separators=(",",":")

                    )



            else:


                payload = ""







            sign_string = (

                timestamp

                +

                self.api_key

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

                    self.api_key,


                "X-BAPI-SIGN":

                    signature,


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






            data = r.json()





            if data.get("retCode") != 0:


                print(

                    "[BYBIT ERROR]",

                    data

                )


                return None






            return data






        except Exception as e:


            print(

                "[API REQUEST ERROR]",

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

                    "60",


                "limit":

                    limit

            }

        )



        if not result:


            return []




        return (

            result

            .get(

                "result",

                {}

            )

            .get(

                "list",

                []

            )

        )











    # =====================================================
    # LAST PRICE
    # =====================================================

    def get_last_price(
        self
    ):


        result = self.request(

            "GET",

            "/v5/market/tickers",

            {


                "category":

                    CATEGORY,


                "symbol":

                    DEFAULT_SYMBOL

            }

        )



        try:


            return float(

                result["result"]["list"][0]["lastPrice"]

            )



        except:


            return None











    # =====================================================
    # POSITION
    # =====================================================

    def get_position(
        self
    ):


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
    # QTY FORMAT
    # =====================================================

    def format_qty(
        self,
        qty
    ):


        step = 0.001


        qty = math.floor(

            qty / step

        ) * step



        return round(

            qty,

            3

        )












    # =====================================================
    # CREATE ORDER
    # =====================================================

    def create_order(
        self,
        side,
        qty
    ):


        qty = self.format_qty(

            qty

        )



        print(

            "[ORDER REQUEST]",

            side,

            qty

        )





        if not LIVE:


            print(

                "[TEST MODE ORDER]"

            )


            return {


                "retCode":

                    0,


                "result":

                    {


                        "orderId":

                            "TEST"

                    }

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
    # TP SL
    # =====================================================

    def set_trading_stop(
        self,
        take_profit,
        stop_loss
    ):



        if not LIVE:


            print(

                "[TEST TP SL]",

                take_profit,

                stop_loss

            )


            return True







        return self.request(

            "POST",

            "/v5/position/trading-stop",

            {


                "category":

                    CATEGORY,


                "symbol":

                    DEFAULT_SYMBOL,


                "takeProfit":

                    str(take_profit),


                "stopLoss":

                    str(stop_loss)

            }

        )









    # =====================================================
    # CLOSE POSITION
    # =====================================================

    def close_position(
        self
    ):


        if not LIVE:


            print(

                "[TEST CLOSE POSITION]"

            )


            return True





        position = self.get_position()



        if not position:


            return False




        rows = (

            position

            ["result"]

            ["list"]

        )




        for p in rows:


            size = float(

                p["size"]

            )



            if size > 0:



                side = p["side"]



                close_side = (

                    "Sell"

                    if side == "Buy"

                    else

                    "Buy"

                )



                return self.create_order(

                    close_side,

                    size

                )



        return False







# =====================================================
# SINGLETON
# =====================================================

bybit_api = BybitAPI()
