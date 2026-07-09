import time
import hmac
import hashlib
import requests


from config import (
    BYBIT_BASE_URL,
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    DEFAULT_SYMBOL,
    LIVE_TRADING,
)



class ExecutionEngine:


    def __init__(self):


        self.base_url = BYBIT_BASE_URL

        self.api_key = BYBIT_API_KEY

        self.api_secret = BYBIT_API_SECRET

        self.symbol = DEFAULT_SYMBOL

        self.live = LIVE_TRADING



        print("==============================")
        print("[EXECUTION ENGINE INIT]")
        print("BASE :", self.base_url)
        print("LIVE :", self.live)
        print("SYMBOL :", self.symbol)
        print("==============================")



    # =====================================
    # SIGN
    # =====================================

    def _sign(
        self,
        params
    ):


        timestamp = str(
            int(
                time.time()*1000
            )
        )


        recv_window = "5000"


        query_string = "&".join(
            [
                f"{k}={params[k]}"
                for k in sorted(params)
            ]
        )


        origin = (
            timestamp
            +
            self.api_key
            +
            recv_window
            +
            query_string
        )


        sign = hmac.new(
            self.api_secret.encode(),
            origin.encode(),
            hashlib.sha256
        ).hexdigest()


        return (
            timestamp,
            recv_window,
            sign
        )



    # =====================================
    # HEADER
    # =====================================

    def _headers(
        self,
        timestamp,
        recv_window,
        sign
    ):


        return {

            "X-BAPI-API-KEY":
                self.api_key,

            "X-BAPI-SIGN":
                sign,

            "X-BAPI-TIMESTAMP":
                timestamp,

            "X-BAPI-RECV-WINDOW":
                recv_window,

            "Content-Type":
                "application/json"

        }



    # =====================================
    # MARKET ORDER
    # =====================================

    def market_order(
        self,
        side,
        qty
    ):


        if not self.live:

            print(
                "[EXECUTION BLOCKED] LIVE=False"
            )

            return None



        endpoint = (
            "/v5/order/create"
        )


        params = {


            "category":
                "linear",


            "symbol":
                self.symbol,


            "side":
                side,


            "orderType":
                "Market",


            "qty":
                str(qty)

        }



        timestamp, recv_window, sign = (
            self._sign(params)
        )



        headers = self._headers(
            timestamp,
            recv_window,
            sign
        )


        url = (
            self.base_url
            +
            endpoint
        )



        try:


            print("[EXECUTION ORDER]")
            print(url)
            print(params)



            response = requests.post(

                url,

                headers=headers,

                json=params,

                timeout=10

            )



            data = response.json()



            print(
                "[EXECUTION RESPONSE]",
                data
            )


            return data



        except Exception as e:


            print(
                "[EXECUTION ERROR]",
                e
            )


            return None



    # =====================================
    # CLOSE POSITION
    # =====================================

    def close_position(
        self,
        side,
        qty
    ):


        close_side = (
            "Sell"
            if side == "Buy"
            else
            "Buy"
        )


        return self.market_order(
            close_side,
            qty
        )



    # =====================================
    # TEST CONNECTION
    # =====================================

    def ping(self):


        try:


            r = requests.get(
                self.base_url
                +
                "/v5/market/time",
                timeout=5
            )


            print(
                "[BYBIT TIME]",
                r.json()
            )


            return True



        except Exception as e:


            print(
                "[PING ERROR]",
                e
            )


            return False




execution_engine = ExecutionEngine()
