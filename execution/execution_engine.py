import os
import time
import hmac
import hashlib
import requests


from dotenv import load_dotenv


from trade_db import trade_db


from risk.trailing_stop_manager import (
    trailing_stop_manager
)


load_dotenv()



class ExecutionEngine:


    def __init__(self):


        self.api_key = os.getenv(

            "BYBIT_API_KEY"

        )


        self.api_secret = os.getenv(

            "BYBIT_API_SECRET"

        )


        self.base_url = os.getenv(

            "BYBIT_BASE_URL",

            "https://api.bybit.com"

        )


        self.retry = int(

            os.getenv(

                "ORDER_RETRY",

                "3"

            )

        )





    # =====================================
    # SIGN
    # =====================================

    def sign(
        self,
        timestamp,
        body
    ):


        recv = "5000"


        payload = (

            timestamp

            +

            self.api_key

            +

            recv

            +

            body

        )


        return hmac.new(

            self.api_secret.encode(),

            payload.encode(),

            hashlib.sha256

        ).hexdigest()





    # =====================================
    # MARKET ORDER
    # =====================================

    def execute(
        self,
        symbol,
        side,
        qty
    ):


        endpoint = "/v5/order/create"


        url = self.base_url + endpoint



        body = {


            "category":

                "linear",


            "symbol":

                symbol,


            "side":

                side,


            "orderType":

                "Market",


            "qty":

                str(qty)

        }



        for i in range(

            self.retry

        ):


            try:


                result = self.request(

                    url,

                    body

                )



                if result.get(

                    "retCode"

                ) == 0:


                    print(

                        "ORDER SUCCESS",

                        result

                    )


                    return result





            except Exception as e:


                print(

                    "ORDER RETRY",

                    i,

                    e

                )



            time.sleep(2)



        return None





    # =====================================
    # CLOSE POSITION
    # =====================================

    def close_position(
        self,
        symbol,
        side,
        qty
    ):


        close_side = (

            "Sell"

            if side == "Buy"

            else

            "Buy"

        )



        body = {


            "category":

                "linear",


            "symbol":

                symbol,


            "side":

                close_side,


            "orderType":

                "Market",


            "qty":

                str(qty),


            "reduceOnly":

                True

        }



        result = self.request(

            self.base_url

            +

            "/v5/order/create",

            body

        )



        if result and result.get(

            "retCode"

        ) == 0:


            trailing_stop_manager.reset(

                symbol

            )



        return result





    # =====================================
    # REQUEST
    # =====================================

    def request(
        self,
        url,
        body
    ):


        timestamp = str(

            int(

                time.time()

                *

                1000

            )

        )


        headers = {


            "X-BAPI-API-KEY":

                self.api_key,


            "X-BAPI-TIMESTAMP":

                timestamp,


            "X-BAPI-RECV-WINDOW":

                "5000"

        }



        raw = str(body).replace(

            "'",

            '"'

        )



        headers["X-BAPI-SIGN"] = self.sign(

            timestamp,

            raw

        )



        r = requests.post(

            url,

            json=body,

            headers=headers,

            timeout=5

        )


        return r.json()





    # =====================================
    # FILL CALLBACK
    # =====================================

    def on_fill(
        self,
        symbol,
        side,
        qty,
        price
    ):


        print(

            "FILL",

            symbol,

            side,

            qty,

            price

        )


        trade_db.insert(

            symbol,

            side,

            qty,

            price,

            0,

            "ENTRY"

        )





    # =====================================
    # TRAILING UPDATE
    # =====================================

    def update_trailing_stop(
        self,
        symbol,
        side,
        price
    ):


        trailing_stop_manager.update(

            symbol,

            side,

            price

        )


        new_sl = trailing_stop_manager.calculate_stop(

            symbol,

            side

        )


        if new_sl:


            self.modify_stop_loss(

                symbol,

                new_sl

            )





    # =====================================
    # MODIFY SL
    # =====================================

    def modify_stop_loss(
        self,
        symbol,
        stop_price
    ):


        body = {


            "category":

                "linear",


            "symbol":

                symbol,


            "stopLoss":

                str(stop_price)

        }



        return self.request(

            self.base_url

            +

            "/v5/position/trading-stop",

            body

        )





    # =====================================
    # EQUITY
    # =====================================

    def get_account_equity(
        self
    ):


        url = (

            self.base_url

            +

            "/v5/account/wallet-balance"

        )


        timestamp = str(

            int(

                time.time()

                *

                1000

            )

        )


        body = {

            "accountType":

                "UNIFIED"

        }



        result = self.request(

            url,

            body

        )



        try:


            return float(

                result["result"]["list"][0]["totalEquity"]

            )


        except:


            return 0





execution_engine = ExecutionEngine()
