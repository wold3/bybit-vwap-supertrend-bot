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
    BYBIT_REST_URL,
    CATEGORY,
    DEFAULT_SYMBOL,
    ACCOUNT_TYPE,
    LEVERAGE
)





class BybitAPI:



    def __init__(self):

        self.base_url = BYBIT_REST_URL


        print(
            "[BYBIT API READY]"
        )





    # =====================================================
    # SIGN
    # =====================================================

    def sign(
        self,
        timestamp,
        payload
    ):


        recv_window = "5000"


        origin = (

            timestamp

            +

            BYBIT_API_KEY

            +

            recv_window

            +

            payload

        )


        return hmac.new(

            BYBIT_API_SECRET.encode(),

            origin.encode(),

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


            if params is None:

                params = {}



            timestamp = str(

                int(

                    time.time()*1000

                )

            )


            recv_window = "5000"




            if method == "GET":


                payload = "&".join(

                    [

                        f"{k}={v}"

                        for k,v in sorted(

                            params.items()

                        )

                    ]

                )



            else:


                payload = json.dumps(

                    params,

                    separators=(

                        ",",

                        ":"

                    )

                )





            signature = self.sign(

                timestamp,

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

                    data=payload,

                    timeout=10

                )





            data = r.json()





            code = data.get(

                "retCode"

            )




            # leverage already set

            if code == 110043:


                return data






            if code != 0:


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
    # PING
    # =====================================================

    def ping(self):


        try:


            r = requests.get(

                self.base_url

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


            if result.get("retCode") == 110043:


                print(

                    "[LEVERAGE ALREADY SET]"

                )


            else:


                print(

                    "[LEVERAGE SET]"

                )



        return result







    # =====================================================
    # KLINE
    # =====================================================

    def get_kline(
        self,
        interval="60"
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

                    interval,


                "limit":

                    200

            }

        )



        if not result:


            return []





        rows = (

            result

            .get("result",{})

            .get("list",[])

        )



        candles = []



        for c in reversed(rows):


            candles.append(

                {


                    "timestamp":

                        int(c[0]),


                    "open":

                        float(c[1]),


                    "high":

                        float(c[2]),


                    "low":

                        float(c[3]),


                    "close":

                        float(c[4]),


                    "volume":

                        float(c[5])

                }

            )



        print(

            "[KLINE]",

            len(candles)

        )


        return candles








    # =====================================================
    # PRICE
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

                result["result"]

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
    # CLOSE
    # =====================================================

    def close_position(self):


        position = self.get_position()



        if not position:


            return False





        rows = (

            position

            .get("result",{})

            .get("list",[])

        )




        for p in rows:


            size = float(

                p.get(

                    "size",

                    0

                )

            )



            if size > 0:



                side = p.get(

                    "side"

                )


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
    # INSTRUMENT
    # =====================================================

    def get_instrument_info(self):


        return self.request(

            "GET",

            "/v5/market/instruments-info",

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


        try:


            info = self.get_instrument_info()



            step = float(

                info["result"]

                ["list"][0]

                ["lotSizeFilter"]

                ["qtyStep"]

            )



            precision = len(

                str(step)

                .split(".")[1]

            )



            qty = (

                int(qty / step)

                *

                step

            )



            return round(

                qty,

                precision

            )



        except Exception as e:


            print(

                "[QTY FORMAT ERROR]",

                e

            )


            return round(

                qty,

                3

            )









    # =====================================================
    # TP / SL
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
# SINGLETON
# =====================================================

bybit_api = BybitAPI()
