import os
import time
import hmac
import hashlib
import requests


from dotenv import load_dotenv


from risk.risk_engine import risk_engine

from risk.drawdown_guard import drawdown_guard

from risk.sltp_manager import sltp_manager


from trade_db import trade_db



load_dotenv()





class BybitExecutionEngine:



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





    # =====================================
    # ORDER
    # =====================================

    def execute(
        self,
        symbol,
        side,
        qty
    ):


        if not risk_engine.can_trade():

            print(
                "BLOCK RISK"
            )

            return None



        if not drawdown_guard.can_trade():

            print(
                "BLOCK DRAWDOWN"
            )

            return None



        return self.send_order(

            symbol,

            side,

            qty

        )





    # =====================================
    # MARKET ORDER
    # =====================================

    def send_order(
        self,
        symbol,
        side,
        qty
    ):


        endpoint = (
            "/v5/order/create"
        )


        url = (

            self.base_url

            +

            endpoint

        )



        timestamp = str(

            int(
                time.time()
                *
                1000
            )

        )



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



        body_text = str(body)



        sign = hmac.new(

            self.api_secret.encode(),

            (

                timestamp

                +

                self.api_key

                +

                "5000"

                +

                body_text

            ).encode(),

            hashlib.sha256

        ).hexdigest()




        headers = {


            "X-BAPI-API-KEY":

                self.api_key,


            "X-BAPI-SIGN":

                sign,


            "X-BAPI-TIMESTAMP":

                timestamp,


            "X-BAPI-RECV-WINDOW":

                "5000"


        }



        response = requests.post(

            url,

            json=body,

            headers=headers

        )



        return response.json()





    # =====================================
    # REAL FILL
    # =====================================

    def on_fill(
        self,
        symbol,
        side,
        qty,
        price
    ):


        print(

            "REAL FILL",

            symbol,

            side,

            qty,

            price

        )



        # 거래 저장

        trade_db.insert(

            symbol,

            side,

            qty,

            price

        )




        # ============================
        # AUTO SL TP
        # ============================


        levels = sltp_manager.calculate(

            side,

            price

        )



        print(

            "AUTO SL TP",

            levels

        )



        self.set_sl_tp(

            symbol,

            side,

            qty,

            levels["stop_loss"],

            levels["take_profit"]

        )





    # =====================================
    # BYBIT TRADING STOP
    # =====================================

    def set_sl_tp(
        self,
        symbol,
        side,
        qty,
        sl,
        tp
    ):


        endpoint = (

            "/v5/position/trading-stop"

        )


        url = (

            self.base_url

            +

            endpoint

        )



        timestamp = str(

            int(
                time.time()
                *
                1000
            )

        )



        body = {


            "category":

                "linear",


            "symbol":

                symbol,


            "stopLoss":

                str(sl),


            "takeProfit":

                str(tp),


            "slTriggerBy":

                "MarkPrice",


            "tpTriggerBy":

                "MarkPrice"

        }



        sign = hmac.new(

            self.api_secret.encode(),

            (

                timestamp

                +

                self.api_key

                +

                "5000"

                +

                str(body)

            ).encode(),

            hashlib.sha256

        ).hexdigest()



        headers = {


            "X-BAPI-API-KEY":

                self.api_key,


            "X-BAPI-SIGN":

                sign,


            "X-BAPI-TIMESTAMP":

                timestamp,


            "X-BAPI-RECV-WINDOW":

                "5000"

        }



        r = requests.post(

            url,

            json=body,

            headers=headers

        )


        print(

            "SL TP RESULT",

            r.json()

        )





execution_engine = BybitExecutionEngine()
