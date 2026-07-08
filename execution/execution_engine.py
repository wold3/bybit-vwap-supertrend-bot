# execution/execution_engine.py

import os
import time
import hmac
import hashlib
import json
import requests

from dotenv import load_dotenv

from trade_db import trade_db
from risk.trailing_stop_manager import trailing_stop_manager
from position.position_manager import position_manager


load_dotenv()



class ExecutionEngine:


    def __init__(self):

        self.api_key = os.getenv(
            "BYBIT_API_KEY",
            ""
        )

        self.api_secret = os.getenv(
            "BYBIT_API_SECRET",
            ""
        )


        self.base_url = os.getenv(
            "BYBIT_BASE_URL",
            "https://api-testnet.bybit.com"
        )


        self.retry = int(
            os.getenv(
                "ORDER_RETRY",
                "3"
            )
        )


        self.recv_window = "10000"

        self.time_offset = 0


        self.sync_time()



    # =====================================
    # TIME SYNC
    # =====================================

    def sync_time(self):

        try:

            r = requests.get(

                self.base_url +
                "/v5/market/time",

                timeout=5

            )


            data = r.json()


            server_time = int(
                data["time"]
            )


            local_time = int(
                time.time()*1000
            )


            self.time_offset = (

                server_time

                -

                local_time

            )


            print(
                "[TIME SYNC]",
                self.time_offset,
                "ms"
            )


        except Exception as e:

            print(
                "[TIME SYNC ERROR]",
                e
            )

            self.time_offset = 0




    # =====================================
    # SIGN
    # =====================================

    def sign(
        self,
        timestamp,
        payload
    ):


        origin = (

            timestamp

            +

            self.api_key

            +

            self.recv_window

            +

            payload

        )


        return hmac.new(

            self.api_secret.encode(),

            origin.encode(),

            hashlib.sha256

        ).hexdigest()



    # =====================================
    # REQUEST
    # =====================================

    def request(
        self,
        url,
        body=None,
        method="POST"
    ):


        body = body or {}


        timestamp = str(

            int(
                time.time()*1000
            )

            +

            self.time_offset

        )


        # GET SIGN

if method.upper() == "GET":

    payload = "&".join(
        sorted(
            [
                f"{k}={v}"
                for k, v in body.items()
            ]
        )
    )


        else:


            payload = json.dumps(

                body,

                separators=(",", ":")

            )



        headers = {


            "Content-Type":

                "application/json",



            "X-BAPI-API-KEY":

                self.api_key,



            "X-BAPI-TIMESTAMP":

                timestamp,



            "X-BAPI-RECV-WINDOW":

                self.recv_window,



            "X-BAPI-SIGN":

                self.sign(

                    timestamp,

                    payload

                )

        }



        try:


            if method.upper()=="GET":


                response = requests.get(

                    url,

                    params=body,

                    headers=headers,

                    timeout=10

                )


            else:


                response = requests.post(

                    url,

                    json=body,

                    headers=headers,

                    timeout=10

                )



            print("====================")

            print("[BYBIT]")

            print(response.text)

            print("====================")



            return response.json()



        except Exception as e:


            print(

                "[REQUEST ERROR]",

                e

            )


            return {}





    # =====================================
    # EXECUTE SIGNAL
    # =====================================

    def execute_signal(
        self,
        signal
    ):


        if not signal:

            return None


        if signal.get("type")=="ENTRY":


            return self.execute(

                signal["symbol"],

                signal["side"],

                signal["qty"]

            )


        elif signal.get("type")=="EXIT":


            return self.close_position(

                signal["symbol"],

                signal["side"],

                signal["qty"]

            )



    # =====================================
    # MARKET ORDER
    # =====================================

    def execute(
        self,
        symbol,
        side,
        qty
    ):


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



        for _ in range(self.retry):


            result = self.request(

                self.base_url+
                "/v5/order/create",

                body

            )


            if result.get("retCode")==0:


                position_manager.open_position(

                    symbol,

                    side,

                    qty

                )


                return result



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

            if side=="Buy"

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

            self.base_url+
            "/v5/order/create",

            body

        )


        if result.get("retCode")==0:


            position_manager.close_position(symbol)

            trailing_stop_manager.reset(symbol)


        return result




    # =====================================
    # WALLET
    # =====================================

    def get_account_equity(
        self
    ):


        result = self.request(

            self.base_url+
            "/v5/account/wallet-balance",

            {

                "accountType":
                    "UNIFIED"

            },

            method="GET"

        )


        try:


            return float(

                result["result"]
                ["list"]
                [0]
                ["totalEquity"]

            )


        except:


            return 0.0



    def get_wallet_balance(self):

        return self.get_account_equity()



    # =====================================
    # STATUS
    # =====================================

    def status(self):


        return {


            "api_key":

                bool(self.api_key),


            "base_url":

                self.base_url,


            "recv_window":

                self.recv_window,


            "time_offset":

                self.time_offset


        }





execution_engine = ExecutionEngine()
