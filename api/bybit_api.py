# =====================================================
# api/bybit_api.py
# Bybit V5 REST API
# =====================================================

import time
import hmac
import hashlib
import json
import requests



from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    BYBIT_REST_URL,
    CATEGORY,
    DEFAULT_SYMBOL,
    ACCOUNT_TYPE,
    LEVERAGE
)







class BybitAPI:



    def __init__(self):

        print("==============================")
        print("[BYBIT API INIT]")
        print("TESTNET :", False)
        print("ACCOUNT :", ACCOUNT_TYPE)
        print("CATEGORY:", CATEGORY)
        print("SYMBOL  :", DEFAULT_SYMBOL)
        print("==============================")







    # =====================================================
    # SIGN
    # =====================================================

    def generate_signature(
        self,
        timestamp,
        payload
    ):


        recv_window = "5000"



        param = (

            str(timestamp)

            +

            BYBIT_API_KEY

            +

            recv_window

            +

            payload

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
        endpoint,
        params=None
    ):


        if params is None:

            params = {}



        timestamp = int(

            time.time()*1000

        )



        recv_window = "5000"



        if method == "GET":


            payload = json.dumps(

                params,

                separators=(",", ":")

            )

        else:


            payload = json.dumps(

                params,

                separators=(",", ":")

            )





        headers = {


            "X-BAPI-API-KEY":

                BYBIT_API_KEY,


            "X-BAPI-SIGN":

                self.generate_signature(

                    timestamp,

                    payload

                ),


            "X-BAPI-TIMESTAMP":

                str(timestamp),


            "X-BAPI-RECV-WINDOW":

                recv_window,


            "Content-Type":

                "application/json"

        }




        url = (

            BYBIT_REST_URL

            +

            endpoint

        )



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

                    data=payload,

                    timeout=10

                )



            data = r.json()



            if data.get(

                "retCode",

                -1

            ) != 0:


                print(

                    "[BYBIT ERROR]",

                    data

                )


                return None



            return data



        except Exception as e:


            print(

                "[REQUEST ERROR]",

                e

            )


            return None







    # =====================================================
    # PING
    # =====================================================

    def ping(self):


        try:


            r = requests.get(

                BYBIT_REST_URL

                +

                "/v5/market/time",

                timeout=5

            )


            return r.status_code == 200



        except:


            return False







    # =====================================================
    # WALLET
    # =====================================================

    def get_wallet_balance(self):


        return self.request(

            "GET",

            "/v5/account/wallet-balance",

            {


                "accountType":

                    ACCOUNT_TYPE


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

                    "1",


                "limit":

                    200

            }

        )



        if not result:


            return []



        rows = (

            result

            .get("result", {})

            .get("list", [])

        )



        candles = []



        for x in reversed(rows):


            candles.append(

                {


                    "timestamp":

                        int(x[0]),


                    "open":

                        float(x[1]),


                    "high":

                        float(x[2]),


                    "low":

                        float(x[3]),


                    "close":

                        float(x[4]),


                    "volume":

                        float(x[5])


                }

            )



        print(

            "[KLINE]",

            len(candles)

        )


        return candles







    # =====================================================
    # LAST PRICE
    # =====================================================

    def get_last_price(self):


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

                result

                ["result"]

                ["list"][0]

                ["lastPrice"]

            )


        except:


            return None







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



        if result:


            print(

                "[LEVERAGE SET]",

                LEVERAGE

            )


        else:


            print(

                "[LEVERAGE ALREADY SET]"

            )



        return result







    # =====================================================
    # CREATE MARKET ORDER
    # =====================================================

    def create_order(
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
    # SET TP SL
    # =====================================================

    def set_trading_stop(
        self,
        take_profit,
        stop_loss
    ):


        return self.request(

            "POST",

            "/v5/position/trading-stop",

            {


                "category":

                    CATEGORY,


                "symbol":

                    DEFAULT_SYMBOL,


                "tpslMode":

                    "Full",


                "positionIdx":

                    0,


                "takeProfit":

                    str(take_profit),


                "stopLoss":

                    str(stop_loss)


            }

        )







    # =====================================================
    # CLOSE POSITION
    # =====================================================

    def close_position(self):


        position = self.get_position()



        if not position:


            return False



        rows = (

            position

            .get("result", {})

            .get("list", [])

        )



        for p in rows:


            size = float(

                p.get(

                    "size",

                    0

                )

            )



            if size > 0:


                close_side = (

                    "Sell"

                    if p.get("side") == "Buy"

                    else "Buy"

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
