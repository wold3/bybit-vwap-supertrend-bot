# =====================================================
# api/bybit_api.py
# BYBIT V5 API MANAGER
# =====================================================

import time
import hmac
import hashlib
import json

import requests

from urllib.parse import urlencode

from requests.adapters import HTTPAdapter

from urllib3.util.retry import Retry


from config import (

    SYMBOL,

    CATEGORY,

    LEVERAGE,

    DEMO_API_KEY,
    DEMO_API_SECRET,

    LIVE_API_KEY,
    LIVE_API_SECRET,

    API_TIMEOUT,
    API_RETRY

)


from web.server import (

    add_log

)





class BybitAPI:


    def __init__(self):


        self.mode = "DEMO"


        self.api_key = DEMO_API_KEY
        self.api_secret = DEMO_API_SECRET


        self.base_url = ""


        self.session = requests.Session()


        retry = Retry(

            total=API_RETRY,

            connect=API_RETRY,

            read=API_RETRY,

            backoff_factor=0.5,

            status_forcelist=[
                429,
                500,
                502,
                503,
                504
            ],

            allowed_methods=[
                "GET",
                "POST"
            ]

        )


        adapter = HTTPAdapter(

            max_retries=retry

        )


        self.session.mount(

            "https://",

            adapter

        )


        self.update_endpoint()


        print(

            "[BYBIT READY]",

            self.mode

        )



    # =====================================================
    # ENDPOINT
    # =====================================================

    def update_endpoint(self):


        if self.mode == "DEMO":


            self.base_url = "https://api-demo.bybit.com"

            self.api_key = DEMO_API_KEY

            self.api_secret = DEMO_API_SECRET


        else:


            self.base_url = "https://api.bybit.com"

            self.api_key = LIVE_API_KEY

            self.api_secret = LIVE_API_SECRET



    # =====================================================
    # MODE CHANGE
    # =====================================================

    def change_session(

        self,

        mode

    ):


        mode = mode.upper()


        if mode not in [

            "DEMO",

            "LIVE"

        ]:

            return False


        self.mode = mode


        self.update_endpoint()


        print(

            "[BYBIT SESSION CHANGE]",

            self.mode

        )


        return True



    # =====================================================
    # SIGN
    # =====================================================

    def sign(

        self,

        timestamp,

        recv_window,

        payload

    ):


        origin = (

            str(timestamp)

            +

            self.api_key

            +

            str(recv_window)

            +

            payload

        )


        signature = hmac.new(

            self.api_secret.encode(

                "utf-8"

            ),

            origin.encode(

                "utf-8"

            ),

            hashlib.sha256

        ).hexdigest()


        return signature

    # =====================================================
    # REQUEST
    # =====================================================

    def request(

        self,

        method,

        path,

        params=None

    ):

        try:

            timestamp = str(

                int(time.time() * 1000)

            )

            recv_window = "5000"

            params = params or {}

            # ---------------------------------
            # GET
            # ---------------------------------

            if method.upper() == "GET":

                query = urlencode(

                    sorted(params.items())

                )

                payload = query

                url = self.base_url + path

                if query:

                    url += "?" + query

            # ---------------------------------
            # POST
            # ---------------------------------

            else:

                payload = json.dumps(

                    params,

                    separators=(",", ":")

                )

                url = self.base_url + path

            signature = self.sign(

                timestamp,

                recv_window,

                payload

            )

            headers = {

                "X-BAPI-API-KEY":

                    self.api_key,

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

            # ---------------------------------
            # SEND
            # ---------------------------------

            if method.upper() == "GET":

                response = self.session.get(

                    url,

                    headers=headers,

                    timeout=API_TIMEOUT

                )

            else:

                response = self.session.post(

                    url,

                    headers=headers,

                    data=payload,

                    timeout=API_TIMEOUT

                )

            # ---------------------------------
            # HTTP ERROR
            # ---------------------------------

            if not response.ok:

                add_log(

                    f"HTTP ERROR {response.status_code}"

                )

                return None

            # ---------------------------------
            # JSON
            # ---------------------------------

            try:

                data = response.json()

            except ValueError:

                add_log(

                    f"INVALID RESPONSE : {response.text[:300]}"

                )

                return None

            # ---------------------------------
            # BYBIT ERROR
            # ---------------------------------

            if data.get("retCode") != 0:

                add_log(

                    f"BYBIT ERROR {data}"

                )

                return None

            return data

        except requests.Timeout:

            add_log(

                "REQUEST TIMEOUT"

            )

            return None

        except requests.ConnectionError:

            add_log(

                "NETWORK ERROR"

            )

            return None

        except Exception as e:

            add_log(

                f"API ERROR {e}"

            )

            return None

    # =====================================================
    # BALANCE
    # =====================================================

    def get_balance(self):

        return self.request(

            "GET",

            "/v5/account/wallet-balance",

            {

                "accountType": "UNIFIED"

            }

        )



    # =====================================================
    # POSITION
    # =====================================================

    def get_position(self):

        return self.request(

            "GET",

            "/v5/position/list",

            {

                "category": CATEGORY,

                "symbol": SYMBOL

            }

        )



    # =====================================================
    # PRICE
    # =====================================================

    def get_price(self):

        data = self.request(

            "GET",

            "/v5/market/tickers",

            {

                "category": CATEGORY,

                "symbol": SYMBOL

            }

        )

        if not data:

            return None

        try:

            return float(

                data["result"]["list"][0]["lastPrice"]

            )

        except Exception:

            return None



    # =====================================================
    # KLINE
    # =====================================================

    def get_kline(

        self,

        interval="5",

        limit=200

    ):

        return self.request(

            "GET",

            "/v5/market/kline",

            {

                "category": CATEGORY,

                "symbol": SYMBOL,

                "interval": interval,

                "limit": limit

            }

        )



    # =====================================================
    # LEVERAGE
    # =====================================================

    def set_leverage(self):

        return self.request(

            "POST",

            "/v5/position/set-leverage",

            {

                "category": CATEGORY,

                "symbol": SYMBOL,

                "buyLeverage": str(LEVERAGE),

                "sellLeverage": str(LEVERAGE)

            }

        )



    # =====================================================
    # MARKET ORDER
    # =====================================================

    def place_order(

        self,

        side,

        qty,

        reduce_only=False

    ):

        body = {

            "category": CATEGORY,

            "symbol": SYMBOL,

            "side": side,

            "orderType": "Market",

            "qty": str(qty),

            "timeInForce": "IOC",

            "reduceOnly": reduce_only

        }

        return self.request(

            "POST",

            "/v5/order/create",

            body

        )



    # =====================================================
    # TP / SL
    # =====================================================

    def set_trading_stop(

        self,

        tp,

        sl

    ):

        body = {

            "category": CATEGORY,

            "symbol": SYMBOL,

            "takeProfit": str(tp),

            "stopLoss": str(sl)

        }

        return self.request(

            "POST",

            "/v5/position/trading-stop",

            body

        )



    # =====================================================
    # CLOSE POSITION
    # =====================================================

    def close_position(self):

        pos = self.get_position()

        if not pos:

            return None

        try:

            item = pos["result"]["list"][0]

            side = item["side"]

            qty = float(item["size"])

        except Exception:

            return None

        if qty <= 0:

            return True

        close_side = "Sell" if side == "Buy" else "Buy"

        return self.place_order(

            close_side,

            qty,

            reduce_only=True

        )



# =====================================================
# INSTANCE
# =====================================================

bybit_api = BybitAPI()
