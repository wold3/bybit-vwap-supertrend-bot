# api/bybit_api.py

import time
from pprint import pprint

from pybit.unified_trading import HTTP

from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    BYBIT_TESTNET,
    BYBIT_DEMO,
    CATEGORY,
    DEFAULT_SYMBOL,
    ACCOUNT_TYPE,
    DEFAULT_QTY,
    ORDER_TYPE,
    TIME_IN_FORCE,
    LEVERAGE,
)


# ==================================================
# BYBIT V5 API CLIENT
# ==================================================

class BybitAPI:


    def __init__(self):

        print("==============================")
        print("[BYBIT API INIT]")
        print("TESTNET :", BYBIT_TESTNET)
        print("DEMO    :", BYBIT_DEMO)
        print("ACCOUNT :", ACCOUNT_TYPE)
        print("CATEGORY:", CATEGORY)
        print("SYMBOL  :", DEFAULT_SYMBOL)
        print("==============================")


        self.session = HTTP(

            testnet=BYBIT_TESTNET,

            demo=BYBIT_DEMO,

            api_key=BYBIT_API_KEY,

            api_secret=BYBIT_API_SECRET,

            recv_window=10000

        )


    # ==================================================
    # SAFE API CALL
    # ==================================================

    def safe_call(
        self,
        func,
        **kwargs
    ):


        retry_count = 3


        for attempt in range(retry_count):

            try:

                response = func(**kwargs)



                if response.get(
                    "retCode"
                ) == 0:

                    return response



                error = response.get(
                    "retMsg"
                )


                print(
                    "[BYBIT ERROR]",
                    error
                )


                # 인증 오류
                if response.get(
                    "retCode"
                ) in [
                    10003,
                    10004
                ]:

                    return None



                time.sleep(2)



            except Exception as e:


                print(
                    "[API EXCEPTION]",
                    attempt + 1,
                    e
                )


                time.sleep(2)



        return None



    # ==================================================
    # WALLET BALANCE
    # ==================================================

    def get_wallet_balance(self):


        response = self.safe_call(

            self.session.get_wallet_balance,

            accountType=ACCOUNT_TYPE

        )


        if not response:

            return None



        try:

            account = (

                response
                ["result"]
                ["list"][0]

            )


            return {

                "equity":

                    float(
                        account["totalEquity"]
                    ),


                "wallet_balance":

                    float(
                        account["totalWalletBalance"]
                    ),


                "available":

                    float(
                        account["totalAvailableBalance"]
                    )

            }



        except Exception as e:


            print(
                "[WALLET PARSE ERROR]",
                e
            )


            return None



    # ==================================================
    # POSITION
    # ==================================================

    def get_position(self):


        response = self.safe_call(

            self.session.get_positions,

            category=CATEGORY,

            symbol=DEFAULT_SYMBOL

        )


        if not response:

            return None



        try:


            positions = (

                response
                ["result"]
                ["list"]

            )


            for pos in positions:


                size = float(

                    pos["size"]

                )


                if size > 0:


                    return {


                        "symbol":

                            pos["symbol"],


                        "side":

                            pos["side"],


                        "size":

                            size,


                        "entry_price":

                            float(
                                pos["avgPrice"]
                            ),


                        "mark_price":

                            float(
                                pos["markPrice"]
                            ),


                        "unrealized_pnl":

                            float(
                                pos["unrealisedPnl"]
                            )

                    }



            return None



        except Exception as e:


            print(
                "[POSITION ERROR]",
                e
            )


            return None



    # ==================================================
    # KLINE
    # ==================================================

    def get_kline(
        self,
        interval="1",
        limit=200
    ):


        response = self.safe_call(

            self.session.get_kline,

            category=CATEGORY,

            symbol=DEFAULT_SYMBOL,

            interval=interval,

            limit=limit

        )


        if not response:

            return None



        try:


            rows = (

                response
                ["result"]
                ["list"]

            )


            candles = []



            for c in reversed(rows):


                candles.append({

                    "time":
                        int(c[0]),

                    "open":
                        float(c[1]),

                    "high":
                        float(c[2]),

                    "low":
                        float(c[3]),

                    "close":
                        float(c[4]),

                    "volume":
                        float(c[5])

                })


            return candles



        except Exception as e:


            print(
                "[KLINE PARSE ERROR]",
                e
            )


            return None



    # ==================================================
    # CURRENT PRICE
    # ==================================================

    def get_price(self):


        response = self.safe_call(

            self.session.get_tickers,

            category=CATEGORY,

            symbol=DEFAULT_SYMBOL

        )


        if not response:

            return None



        try:


            return float(

                response
                ["result"]
                ["list"][0]
                ["lastPrice"]

            )


        except:


            return None



    # ==================================================
    # LEVERAGE
    # ==================================================

    def set_leverage(self):


        response = self.safe_call(

            self.session.set_leverage,

            category=CATEGORY,

            symbol=DEFAULT_SYMBOL,

            buyLeverage=str(LEVERAGE),

            sellLeverage=str(LEVERAGE)

        )


        if response:

            print(
                "[LEVERAGE SET]"
            )

            return True



        return False



    # ==================================================
    # CREATE ORDER
    # ==================================================

    def create_order(
        self,
        side,
        qty=None,
        take_profit=None,
        stop_loss=None,
        reduce_only=False
    ):


        if qty is None:

            qty = DEFAULT_QTY



        params = {


            "category":

                CATEGORY,


            "symbol":

                DEFAULT_SYMBOL,


            "side":

                side,


            "orderType":

                ORDER_TYPE,


            "qty":

                str(qty),


            "timeInForce":

                TIME_IN_FORCE

        }



        if reduce_only:

            params["reduceOnly"] = True



        if take_profit:

            params["takeProfit"] = str(
                round(
                    float(take_profit),
                    2
                )
            )


            params["tpTriggerBy"] = "LastPrice"



        if stop_loss:

            params["stopLoss"] = str(
                round(
                    float(stop_loss),
                    2
                )
            )


            params["slTriggerBy"] = "LastPrice"



        print("==============================")
        print("[ORDER REQUEST]")
        pprint(params)
        print("==============================")


        response = self.safe_call(

            self.session.place_order,

            **params

        )


        return response



    # ==================================================
    # CLOSE POSITION
    # ==================================================

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


        return self.create_order(

            side=close_side,

            qty=qty,

            reduce_only=True

        )



    # ==================================================
    # CANCEL ALL ORDERS
    # ==================================================

    def cancel_all_orders(self):


        return self.safe_call(

            self.session.cancel_all_orders,

            category=CATEGORY,

            symbol=DEFAULT_SYMBOL

        )



    # ==================================================
    # OPEN ORDERS
    # ==================================================

    def get_open_orders(self):


        return self.safe_call(

            self.session.get_open_orders,

            category=CATEGORY,

            symbol=DEFAULT_SYMBOL

        )



    # ==================================================
    # ORDER HISTORY
    # ==================================================

    def get_order_history(
        self,
        order_id=None
    ):


        params = {


            "category":

                CATEGORY,


            "symbol":

                DEFAULT_SYMBOL

        }



        if order_id:

            params["orderId"] = order_id



        return self.safe_call(

            self.session.get_order_history,

            **params

        )



    # ==================================================
    # SERVER TIME
    # ==================================================

    def get_server_time(self):


        return self.safe_call(

            self.session.get_server_time

        )



    # ==================================================
    # HEALTH CHECK
    # ==================================================

    def ping(self):


        try:


            price = self.get_price()


            return price is not None



        except:


            return False



# ==================================================
# SINGLETON
# ==================================================

bybit_api = BybitAPI()
