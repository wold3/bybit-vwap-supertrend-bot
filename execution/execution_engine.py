# execution/execution_engine.py

import os
import time
import hmac
import hashlib
import json
import requests


from dotenv import load_dotenv


from trade_db import trade_db

from position.position_manager import position_manager

from risk.risk_engine import risk_engine

from risk.trailing_stop_manager import trailing_stop_manager



load_dotenv()



class ExecutionEngine:
    """
    Execution Engine

    기능:
    - Bybit 주문 실행
    - Entry / Exit 처리
    - Position 관리
    - Trade DB 기록
    - Trailing Stop 관리
    """



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


        recv_window = "5000"


        payload = (

            timestamp

            +

            self.api_key

            +

            recv_window

            +

            body

        )


        return hmac.new(

            self.api_secret.encode(),

            payload.encode(),

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


        timestamp = str(

            int(
                time.time() * 1000
            )

        )


        recv_window = "5000"


        body = body or {}



        body_json = json.dumps(

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

                recv_window,


            "X-BAPI-SIGN":

                self.sign(

                    timestamp,

                    body_json

                    if method.upper()=="POST"

                    else ""

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



            print("============================")
            print("METHOD :", method)
            print("URL    :", url)
            print("BODY   :", body)
            print("RESULT :", response.text)
            print("============================")



            response.raise_for_status()


            return response.json()



        except Exception as e:


            print(

                "[REQUEST ERROR]",

                e

            )


            return {}





    # =====================================
    # SIGNAL ENTRY POINT
    # =====================================

    def execute_signal(
        self,
        signal
    ):


        if not signal:

            return None



        if signal["type"] == "ENTRY":


            return self.execute(

                signal["symbol"],

                signal["side"],

                signal["qty"]

            )



        if signal["type"] == "EXIT":


            return self.close_position(

                signal["symbol"],

                signal["side"],

                signal["qty"]

            )


        return None





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



        for attempt in range(

            self.retry

        ):



            result = self.request(

                self.base_url

                +

                "/v5/order/create",

                body

            )



            if result.get(

                "retCode"

            ) == 0:



                print(

                    "[ORDER SUCCESS]",

                    result

                )



                position_manager.set_position(

                    symbol,

                    side,

                    qty

                )



                risk_engine.register_trade()



                trade_db.insert_trade(

                    symbol=symbol,

                    side=side,

                    qty=qty,

                    price=0,

                    pnl=0,

                    trade_type="ENTRY"

                )



                return result



            print(

                "[ORDER FAILED]",

                result

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

            self.base_url

            +

            "/v5/order/create",

            body

        )



        if result.get(

            "retCode"

        ) == 0:



            print(

                "[POSITION CLOSED]"

            )



            position_manager.remove_position(

                symbol

            )



            trailing_stop_manager.reset(

                symbol

            )



            trade_db.insert_trade(

                symbol=symbol,

                side=close_side,

                qty=qty,

                price=0,

                pnl=0,

                trade_type="EXIT"

            )



        return result





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

            "[FILL]",

            symbol,

            side,

            qty,

            price

        )



        trade_db.insert_trade(

            symbol=symbol,

            side=side,

            qty=qty,

            price=price,

            pnl=0,

            trade_type="FILL"

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


        try:


            trailing_stop_manager.update(

                symbol,

                side,

                price

            )


            stop_price = trailing_stop_manager.calculate_stop(

                symbol,

                side

            )



            if stop_price:


                self.modify_stop_loss(

                    symbol,

                    stop_price

                )



        except Exception as e:


            print(

                "[TRAIL ERROR]",

                e

            )





    # =====================================
    # MODIFY STOP LOSS
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


        result = self.request(

            self.base_url

            +

            "/v5/account/wallet-balance",

            {

                "accountType":

                    "UNIFIED"

            },

            method="GET"

        )



        try:


            account = result["result"]["list"][0]


            return float(

                account.get(

                    "totalEquity",

                    0

                )

            )



        except Exception:


            return 0.0





    def get_wallet_balance(
        self
    ):


        return self.get_account_equity()





    # =====================================
    # STATUS
    # =====================================

    def status(self):


        return {


            "api_key":

                bool(self.api_key),


            "api_secret":

                bool(self.api_secret),


            "base_url":

                self.base_url,


            "retry":

                self.retry

        }





execution_engine = ExecutionEngine()
