import os
import time
import json
import hmac
import hashlib
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

            self.base_url = os.getenv(
                "BYBIT_LIVE_API",
                "https://api.bybit.com"
            )

        else:

            self.base_url = os.getenv(
                "BYBIT_DEMO_API",
                "https://api-demo.bybit.com"
            )



        self.api_key = os.getenv(
            "BYBIT_API_KEY",
            ""
        )


        self.api_secret = os.getenv(
            "BYBIT_API_SECRET",
            ""
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

    def _sign(
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

    def _request(
        self,
        endpoint,
        payload
    ):


        body = json.dumps(
            payload
        )


        timestamp = int(
            time.time()*1000
        )


        recv_window = 5000


        headers = {


            "X-BAPI-API-KEY":

                self.api_key,


            "X-BAPI-TIMESTAMP":

                str(timestamp),


            "X-BAPI-RECV-WINDOW":

                str(recv_window),


            "X-BAPI-SIGN":

                self._sign(

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



        try:


            r = requests.post(

                url,

                headers=headers,

                data=body,

                timeout=10

            )


            result = r.json()


            print(
                "[ORDER RESPONSE]",
                result
            )


            return result



        except Exception as e:


            print(
                "[ORDER ERROR]",
                e
            )


            return None





    # =====================================
    # EXECUTE SIGNAL
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



        if signal["type"] == "EXIT":


            self.close_position()


            return



        if signal["type"] != "ENTRY":

            return



        side = signal["side"]



        # 중복 포지션 방지

        if self.position == side:


            print(
                "[SKIP SAME POSITION]",
                side
            )


            return





        order_side = side



        payload = {


            "category":

                self.category,


            "symbol":

                self.symbol,


            "side":

                order_side,


            "orderType":

                "Market",


            "qty":

                str(self.qty),


            "timeInForce":

                "IOC"

        }



        print(
            "[ORDER SEND]",
            payload
        )



        result = self._request(

            "/v5/order/create",

            payload

        )



        if result and result.get(
            "retCode"
        ) == 0:


            self.position = side


            print(
                "[POSITION OPEN]",
                side
            )





    # =====================================
    # CLOSE
    # =====================================

    def close_position(
        self
    ):


        if self.position is None:


            print(
                "[NO POSITION]"
            )


            return



        close_side = (

            "Sell"

            if self.position == "Buy"

            else

            "Buy"

        )



        payload = {


            "category":

                self.category,


            "symbol":

                self.symbol,


            "side":

                close_side,


            "orderType":

                "Market",


            "qty":

                str(self.qty),


            "reduceOnly":

                True


        }



        print(
            "[CLOSE ORDER]",
            payload
        )



        result = self._request(

            "/v5/order/create",

            payload

        )



        if result and result.get(
            "retCode"
        ) == 0:


            self.position = None


            print(
                "[POSITION CLOSED]"
            )





    # =====================================
    # STATUS
    # =====================================

    def status(self):


        return {


            "live":

                self.live,


            "symbol":

                self.symbol,


            "position":

                self.position

        }





order_manager = OrderManager()
