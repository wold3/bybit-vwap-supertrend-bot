import os
import time
import hmac
import hashlib
import json
import requests

from dotenv import load_dotenv


load_dotenv()



class OrderManager:


    def __init__(self):


        self.live = (
            os.getenv(
                "LIVE_TRADING",
                "false"
            ).lower()
            ==
            "true"
        )


        if self.live:

            self.base_url = (
                "https://api.bybit.com"
            )

        else:

            self.base_url = (
                "https://api-demo.bybit.com"
            )



        self.api_key = os.getenv(
            "BYBIT_API_KEY"
        )


        self.api_secret = os.getenv(
            "BYBIT_API_SECRET"
        )


        self.symbol = os.getenv(
            "DEFAULT_SYMBOL",
            "BTCUSDT"
        )


        self.category = "linear"


        self.qty = os.getenv(
            "ORDER_QTY",
            "0.001"
        )


        self.position = None




    # =====================================
    # SIGN
    # =====================================

    def sign(
        self,
        timestamp,
        recv_window,
        body
    ):


        param = (
            str(timestamp)
            +
            self.api_key
            +
            str(recv_window)
            +
            body
        )


        return hmac.new(

            self.api_secret.encode(),

            param.encode(),

            hashlib.sha256

        ).hexdigest()





    # =====================================
    # REQUEST
    # =====================================

    def request(
        self,
        endpoint,
        payload
    ):


        timestamp = int(
            time.time()*1000
        )


        recv_window = "5000"


        body = json.dumps(
            payload
        )



        headers = {


            "X-BAPI-API-KEY":

                self.api_key,


            "X-BAPI-TIMESTAMP":

                str(timestamp),


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



        url = (
            self.base_url
            +
            endpoint
        )



        response = requests.post(

            url,

            headers=headers,

            data=body,

            timeout=10

        )


        return response.json()





    # =====================================
    # MARKET ORDER
    # =====================================

    def market_order(
        self,
        side
    ):


        payload = {


            "category":

                self.category,


            "symbol":

                self.symbol,


            "side":

                side,


            "orderType":

                "Market",


            "qty":

                str(self.qty),


            "timeInForce":

                "IOC"

        }



        result = self.request(

            "/v5/order/create",

            payload

        )



        print(
            "[ORDER RESULT]",
            result
        )


        return result





    # =====================================
    # SIGNAL HANDLER
    # =====================================

    def execute(
        self,
        signal
    ):


        if signal is None:

            return



        print(
            "[SIGNAL]",
            signal
        )



        signal_type = signal.get(
            "type"
        )


        side = signal.get(
            "side"
        )



        # ==========================
        # ENTRY
        # ==========================

        if signal_type == "ENTRY":


            if self.position == side:


                print(
                    "[SKIP] SAME POSITION"
                )

                return



            result = self.market_order(

                side

            )


            self.position = side



            print(

                "[POSITION OPEN]",

                side

            )


            return result





        # ==========================
        # EXIT
        # ==========================

        if signal_type == "EXIT":


            if self.position is None:

                return



            close_side = (

                "Sell"

                if self.position == "Buy"

                else

                "Buy"

            )



            result = self.market_order(

                close_side

            )



            print(

                "[POSITION CLOSED]",

                self.position

            )


            self.position = None



            return result





    # =====================================
    # STATUS
    # =====================================

    def status(self):


        return {


            "symbol":

                self.symbol,


            "live":

                self.live,


            "position":

                self.position


        }





order_manager = OrderManager()
