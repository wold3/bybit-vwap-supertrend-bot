import time

from pybit.unified_trading import HTTP

from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    CATEGORY,
    DEFAULT_SYMBOL,
    ACCOUNT_TYPE,
    DEFAULT_QTY,
    ORDER_TYPE,
    TIME_IN_FORCE,
)



# ==================================================
# BYBIT V5 API CLIENT
# ==================================================

class BybitAPI:


    def __init__(self):

        print("==============================")
        print("[BYBIT API INIT]")
        print("BASE : https://api-demo.bybit.com")
        print("TESTNET : False")
        print("DEMO : True")
        print("ACCOUNT :", ACCOUNT_TYPE)
        print("CATEGORY :", CATEGORY)
        print("SYMBOL :", DEFAULT_SYMBOL)
        print("==============================")


        self.session = HTTP(

            testnet=False,

            demo=True,

            api_key=BYBIT_API_KEY,

            api_secret=BYBIT_API_SECRET

        )



    # ==================================================
    # WALLET BALANCE
    # ==================================================

    def get_wallet_balance(self):

        try:

            response = self.session.get_wallet_balance(

                accountType=ACCOUNT_TYPE

            )


            print("[WALLET RESPONSE]")

            return response



        except Exception as e:

            print(
                "[WALLET ERROR]",
                e
            )

            return None



    # ==================================================
    # POSITION
    # ==================================================

    def get_position(self):

        try:

            response = self.session.get_positions(

                category=CATEGORY,

                symbol=DEFAULT_SYMBOL

            )


            return response



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


        try:


            response = self.session.get_kline(

                category=CATEGORY,

                symbol=DEFAULT_SYMBOL,

                interval=interval,

                limit=limit

            )


            return response



        except Exception as e:


            print(
                "[KLINE ERROR]",
                e
            )


            return None



    # ==================================================
    # CREATE ORDER
    # ==================================================

    def create_order(

        self,

        side,

        qty=None

    ):


        try:


            if qty is None:

                qty = DEFAULT_QTY



            response = self.session.place_order(

                category=CATEGORY,

                symbol=DEFAULT_SYMBOL,

                side=side,

                orderType=ORDER_TYPE,

                qty=str(qty),

                timeInForce=TIME_IN_FORCE

            )



            print("[ORDER RESPONSE]")

            print(response)



            return response



        except Exception as e:


            print(
                "[ORDER ERROR]",
                e
            )


            return None



    # ==================================================
    # CANCEL ALL ORDERS
    # ==================================================

    def cancel_all_orders(self):


        try:


            response = self.session.cancel_all_orders(

                category=CATEGORY,

                symbol=DEFAULT_SYMBOL

            )


            print("[CANCEL RESPONSE]")

            print(response)


            return response



        except Exception as e:


            print(
                "[CANCEL ERROR]",
                e
            )


            return None



    # ==================================================
    # SERVER TIME
    # ==================================================

    def server_time(self):


        return int(

            time.time() * 1000

        )




# ==================================================
# SINGLETON
# ==================================================

bybit_api = BybitAPI()
