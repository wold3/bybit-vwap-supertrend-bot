import os
import time
import hmac
import hashlib
import requests

from dotenv import load_dotenv


from risk.risk_engine import risk_engine
from risk.drawdown_guard import drawdown_guard
from risk.sltp_manager import sltp_manager
from risk.trailing_stop_manager import trailing_stop_manager

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
    # PRIVATE SIGN
    # =====================================

    def _sign(
        self,
        timestamp,
        body
    ):


        raw = (

            timestamp

            +

            self.api_key

            +

            "5000"

            +

            str(body)

        )


        return hmac.new(

            self.api_secret.encode(),

            raw.encode(),

            hashlib.sha256

        ).hexdigest()





    # =====================================
    # ORDER EXECUTE
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


        endpoint = "/v5/order/create"


        url = self.base_url + endpoint



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



        headers = {


            "X-BAPI-API-KEY":

                self.api_key,


            "X-BAPI-SIGN":

                self._sign(
                    timestamp,
                    body
                ),


            "X-BAPI-TIMESTAMP":

                timestamp,


            "X-BAPI-RECV-WINDOW":

                "5000"

        }



        r = requests.post(

            url,

            json=body,

            headers=headers,

            timeout=5

        )


        return r.json()





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


        trade_db.insert(

            symbol,

            side,

            qty,

            price

        )



        levels = sltp_manager.calculate(

            side,

            price

        )



        self.set_sl_tp(

            symbol,

            levels["stop_loss"],

            levels["take_profit"]

        )





    # =====================================
    # INITIAL SL TP
    # =====================================

    def set_sl_tp(
        self,
        symbol,
        sl,
        tp
    ):


        self._trading_stop(

            symbol,

            stop_loss=sl,

            take_profit=tp

        )





    # =====================================
    # TRAILING STOP UPDATE
    # =====================================

    def update_trailing_stop(
        self,
        symbol,
        side,
        price
    ):


        new_sl = trailing_stop_manager.update(

            symbol,

            side,

            price

        )


        if not new_sl:

            return



        print(

            "TRAILING MOVE",

            symbol,

            new_sl

        )


        self.move_stop_loss(

            symbol,

            new_sl

        )





    # =====================================
    # MOVE SL
    # =====================================

    def move_stop_loss(
        self,
        symbol,
        stop_loss
    ):


        self._trading_stop(

            symbol,

            stop_loss=stop_loss

        )





    # =====================================
    # BYBIT TRADING STOP API
    # =====================================

    def _trading_stop(
        self,
        symbol,
        stop_loss=None,
        take_profit=None
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

                symbol

        }



        if stop_loss:

            body["stopLoss"] = str(
                stop_loss
            )


            body["slTriggerBy"] = (
                "MarkPrice"
            )



        if take_profit:

            body["takeProfit"] = str(
                take_profit
            )


            body["tpTriggerBy"] = (
                "MarkPrice"
            )



        headers = {


            "X-BAPI-API-KEY":

                self.api_key,


            "X-BAPI-SIGN":

                self._sign(
                    timestamp,
                    body
                ),


            "X-BAPI-TIMESTAMP":

                timestamp,


            "X-BAPI-RECV-WINDOW":

                "5000"

        }



        try:


            r = requests.post(

                url,

                json=body,

                headers=headers,

                timeout=5

            )


            print(

                "TRADING STOP",

                r.json()

            )


        except Exception as e:


            print(

                "TRADING STOP ERROR",

                e

            )





execution_engine = BybitExecutionEngine()
