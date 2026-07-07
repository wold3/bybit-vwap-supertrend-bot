import os
import time
import hmac
import hashlib
import requests

from dotenv import load_dotenv


from risk.risk_engine import risk_engine
from risk.drawdown_guard import drawdown_guard


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



    # =================================================
    # PUBLIC EXECUTE
    # =================================================

    def execute(
        self,
        symbol,
        side,
        qty
    ):


        return self._execute_order(

            symbol,

            side,

            qty

        )



    # =================================================
    # ORDER CHECK + SEND
    # =================================================

    def _execute_order(
        self,
        symbol,
        side,
        qty
    ):


        # -----------------------------
        # Risk Check
        # -----------------------------

        if not risk_engine.can_trade():

            print(
                "[BLOCK] RISK ENGINE"
            )

            return None



        # -----------------------------
        # Drawdown Check
        # -----------------------------

        if not drawdown_guard.can_trade():

            print(
                "[BLOCK] DRAWDOWN"
            )

            return None



        # -----------------------------
        # SEND ORDER
        # -----------------------------

        result = self.send_order(

            symbol,

            side,

            qty

        )


        print(
            "[ORDER RESULT]",
            result
        )


        return result





    # =================================================
    # BYBIT V5 ORDER
    # =================================================

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
            str(qty),


            "timeInForce":
            "IOC"

        }



        body_str = (
            str(body)
        )



        sign_string = (

            timestamp

            +

            self.api_key

            +

            "5000"

            +

            body_str

        )



        signature = hmac.new(

            self.api_secret.encode(),

            sign_string.encode(),

            hashlib.sha256

        ).hexdigest()



        headers = {


            "X-BAPI-API-KEY":
            self.api_key,


            "X-BAPI-SIGN":
            signature,


            "X-BAPI-TIMESTAMP":
            timestamp,


            "X-BAPI-RECV-WINDOW":
            "5000"


        }



        try:


            res = requests.post(

                url,

                json=body,

                headers=headers,

                timeout=5

            )


            return res.json()



        except Exception as e:


            print(

                "[ORDER ERROR]",

                e

            )


            return None





    # =================================================
    # REAL FILL CALLBACK
    # Private WebSocket → 호출
    # =================================================

    def on_fill(
        self,
        symbol,
        side,
        qty,
        price
    ):


        print(
            """
========================
REAL EXECUTION FILL
========================
Symbol :
{}
Side :
{}
Qty :
{}
Price :
{}
========================
""".format(

                symbol,

                side,

                qty,

                price

            )
        )



        # -----------------------------
        # DB 저장
        # -----------------------------

        trade_db.insert(

            symbol=symbol,

            side=side,

            qty=qty,

            price=price

        )



    # =================================================
    # POSITION CLOSE
    # =================================================

    def close_position(
        self,
        symbol
    ):


        print(
            "[CLOSE POSITION]",
            symbol
        )


        # Private position 조회 후
        # reduceOnly 주문 연결 자리



    # =================================================
    # PARTIAL CLOSE
    # =================================================

    def partial_close(
        self,
        symbol,
        percent
    ):


        print(

            "[PARTIAL CLOSE]",

            symbol,

            percent

        )



    # =================================================
    # MOVE STOP LOSS TO BE
    # =================================================

    def move_sl_to_be(
        self,
        symbol
    ):


        print(

            "[MOVE SL TO BE]",

            symbol

        )





# =================================================
# SINGLETON
# =================================================

execution_engine = BybitExecutionEngine()
