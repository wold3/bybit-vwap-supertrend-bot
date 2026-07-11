# =====================================================
# api/bybit_api.py
# BYBIT V5 API MANAGER
# =====================================================

import time
import hmac
import hashlib
import json
import requests


from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    SYMBOL,
    CATEGORY,
    LEVERAGE
)



from web.server import (
    add_log
)







class BybitAPI:


    def __init__(self):


        self.mode = "DEMO"


        self.session = requests.Session()


        self.update_endpoint()



        print(

            "[BYBIT READY]",

            self.mode

        )









    # =====================================================
    # ENDPOINT
    # =====================================================

    def update_endpoint(self):


        if self.mode == "DEMO":


            self.base_url = (

                "https://api-demo.bybit.com"

            )


        else:


            self.base_url = (

                "https://api.bybit.com"

            )








    # =====================================================
    # MODE CHANGE
    # =====================================================

    def change_session(

        self,

        mode

    ):


        self.mode = mode.upper()


        self.update_endpoint()



        print(

            "[BYBIT SESSION CHANGE]",

            self.mode

        )









    # =====================================================
    # SIGN
    # =====================================================

    def sign(

        self,

        timestamp,

        recv_window,

        payload

    ):


        origin = (

            str(timestamp)

            +

            BYBIT_API_KEY

            +

            str(recv_window)

            +

            payload

        )



        signature = hmac.new(

            bytes(

                BYBIT_API_SECRET,

                "utf-8"

            ),

            bytes(

                origin,

                "utf-8"

            ),

            hashlib.sha256

        ).hexdigest()



        return signature









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



            recv_window = "5000"





            if method == "GET":



                query = ""



                if params:


                    query = "&".join(

                        [

                            f"{k}={v}"

                            for k,v in sorted(

                                params.items()

                            )

                        ]

                    )



                payload = query



                url = (

                    self.base_url

                    +

                    path

                )



                if query:


                    url += "?" + query







            else:



                payload = json.dumps(

                    params or {},

                    separators=(

                        ",",

                        ":"

                    )

                )



                url = (

                    self.base_url

                    +

                    path

                )








            signature = self.sign(

                timestamp,

                recv_window,

                payload

            )







            headers = {


                "X-BAPI-API-KEY":

                    BYBIT_API_KEY,


                "X-BAPI-SIGN":

                    signature,


                "X-BAPI-SIGN-TYPE":

                    "2",


                "X-BAPI-TIMESTAMP":

                    timestamp,


                "X-BAPI-RECV-WINDOW":

                    recv_window,


                "Content-Type":

                    "application/json"


            }







            if method == "GET":


                r = self.session.get(

                    url,

                    headers=headers,

                    timeout=10

                )


            else:


                r = self.session.post(

                    url,

                    headers=headers,

                    data=payload,

                    timeout=10

                )







            data = r.json()



            if data.get("retCode") != 0:


                add_log(

                    f"BYBIT ERROR {data}"

                )


                return None





            return data





        except Exception as e:


            add_log(

                f"API ERROR {e}"

            )


            return None










    # =====================================================
    # BALANCE
    # =====================================================

    def get_balance(self):


        return self.request(

            "GET",

            "/v5/account/wallet-balance",

            {

                "accountType":

                    "UNIFIED"

            }

        )









    # =====================================================
    # PRICE
    # =====================================================

    def get_price(self):


        data = self.request(

            "GET",

            "/v5/market/tickers",

            {

                "category":

                    CATEGORY,


                "symbol":

                    SYMBOL

            }

        )



        try:


            return float(

                data["result"]

                ["list"][0]

                ["lastPrice"]

            )


        except:


            return 0









    # =====================================================
    # KLINE
    # =====================================================

    def get_kline(

        self,

        interval="5",

        limit=200

    ):


        return self.request(

            "GET",

            "/v5/market/kline",

            {


                "category":

                    CATEGORY,


                "symbol":

                    SYMBOL,


                "interval":

                    interval,


                "limit":

                    limit

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


        body = {


            "category":

                CATEGORY,


            "symbol":

                SYMBOL,


            "side":

                side,


            "orderType":

                "Market",


            "qty":

                str(qty),


            "timeInForce":

                "IOC"

        }





        return self.request(

            "POST",

            "/v5/order/create",

            body

        )









    # =====================================================
    # TP SL
    # =====================================================

    def set_trading_stop(

        self,

        tp,

        sl

    ):



        body = {


            "category":

                CATEGORY,


            "symbol":

                SYMBOL,


            "takeProfit":

                str(tp),


            "stopLoss":

                str(sl)

        }





        return self.request(

            "POST",

            "/v5/position/trading-stop",

            body

        )









    # =====================================================
    # CLOSE
    # =====================================================

    def close_position(self):


        return self.request(

            "POST",

            "/v5/order/create",

            {


                "category":

                    CATEGORY,


                "symbol":

                    SYMBOL,


                "side":

                    "Sell",


                "orderType":

                    "Market",


                "qty":

                    "0",


                "reduceOnly":

                    True

            }

        )









# =====================================================
# INSTANCE
# =====================================================

bybit_api = BybitAPI()
