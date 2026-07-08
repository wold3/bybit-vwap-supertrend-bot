import os
import time
import hmac
import hashlib
import json
import requests

from dotenv import load_dotenv

from trade_db import trade_db
from risk.trailing_stop_manager import trailing_stop_manager

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
            + self.api_key
            + recv_window
            + body
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
            int(time.time() * 1000)
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
                    body_json if method == "POST" else ""
                )

        }

        try:

            if method.upper() == "GET":

                r = requests.get(

                    url,

                    params=body,

                    headers=headers,

                    timeout=10

                )

            else:

                r = requests.post(

                    url,

                    json=body,

                    headers=headers,

                    timeout=10

                )

            print("===================================")
            print("REQUEST :", method, url)
            print("STATUS  :", r.status_code)
            print("BODY    :", body)
            print("TEXT    :", r.text)
            print("===================================")

            r.raise_for_status()

            return r.json()

        except Exception as e:

            print("[REQUEST ERROR]", e)

            return {}

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

        "category": "linear",

        "symbol": symbol,

        "side": side,

        "orderType": "Market",

        "qty": str(qty)

    }

    for i in range(self.retry):

        try:

            result = self.request(

                url,

                body,

                method="POST"

            )

            if result.get("retCode") == 0:

                print("[ORDER SUCCESS]")

                print(result)

                return result

            print("[ORDER FAILED]")

            print(result)

        except Exception as e:

            print(

                "[ORDER RETRY]",

                i + 1,

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

        "category": "linear",

        "symbol": symbol,

        "side": close_side,

        "orderType": "Market",

        "qty": str(qty),

        "reduceOnly": True

    }

    result = self.request(

        self.base_url + "/v5/order/create",

        body,

        method="POST"

    )

    if result.get("retCode") == 0:

        try:

            trailing_stop_manager.reset(symbol)

        except Exception as e:

            print(

                "[TRAIL RESET ERROR]",

                e

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

    try:

        # 프로젝트 버전 호환
        if hasattr(trade_db, "insert_trade"):

            trade_db.insert_trade(

                symbol=symbol,

                side=side,

                qty=qty,

                price=price,

                pnl=0,

                trade_type="ENTRY"

            )

        elif hasattr(trade_db, "insert"):

            trade_db.insert(

                symbol,

                side,

                qty,

                price,

                0,

                "ENTRY"

            )

    except Exception as e:

        print(

            "[TRADE DB ERROR]",

            e

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

        if stop_price is not None:

            self.modify_stop_loss(

                symbol,

                stop_price

            )

    except Exception as e:

        print(

            "[TRAILING STOP ERROR]",

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

        "category": "linear",

        "symbol": symbol,

        "stopLoss": str(stop_price)

    }

    return self.request(

        self.base_url + "/v5/position/trading-stop",

        body,

        method="POST"

    )

# =====================================
# ACCOUNT EQUITY
# =====================================

def get_account_equity(self):

    url = self.base_url + "/v5/account/wallet-balance"

    params = {
        "accountType": "UNIFIED"
    }

    try:

        result = self.request(

            url,

            params,

            method="GET"

        )

        if result.get("retCode") != 0:

            print("[EQUITY ERROR]")

            print(result)

            return 0.0

        account = result["result"]["list"][0]

        # Unified Account 대응
        if "totalEquity" in account:
            return float(account["totalEquity"])

        # 혹시 구조가 다른 경우
        coin_list = account.get("coin", [])

        if coin_list:

            equity = coin_list[0].get(
                "equity",
                0
            )

            return float(equity)

        return 0.0

    except Exception as e:

        print(

            "[GET EQUITY ERROR]",

            e

        )

        return 0.0


# =====================================
# ACCOUNT BALANCE
# =====================================

def get_wallet_balance(self):

    return self.get_account_equity()


# =====================================
# HEALTH CHECK
# =====================================

def status(self):

    return {

        "api_key": bool(self.api_key),

        "api_secret": bool(self.api_secret),

        "base_url": self.base_url,

        "retry": self.retry

    }


# =====================================
# SINGLETON
# =====================================

execution_engine = ExecutionEngine()
