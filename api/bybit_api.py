import time

from pybit.unified_trading import HTTP

from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    BYBIT_BASE_URL,
    BYBIT_TESTNET,
    CATEGORY,
    DEFAULT_SYMBOL,
    ACCOUNT_TYPE,
)


class BybitAPI:


    def __init__(self):

        print("==============================")
        print("[BYBIT API INIT]")
        print("BASE :", BYBIT_BASE_URL)
        print("TESTNET :", BYBIT_TESTNET)
        print("ACCOUNT :", ACCOUNT_TYPE)
        print("==============================")


        self.session = HTTP(
            testnet=BYBIT_TESTNET,
            api_key=BYBIT_API_KEY,
            api_secret=BYBIT_API_SECRET,
            demo=True
        )



    # ==================================================
    # WALLET
    # ==================================================

    def get_wallet_balance(self):

        try:

            result = self.session.get_wallet_balance(

                accountType=ACCOUNT_TYPE

            )


            print("[WALLET RESPONSE]")
            print(result)


            return result



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

            result = self.session.get_positions(

                category=CATEGORY,

                symbol=DEFAULT_SYMBOL

            )


            return result



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
        interval="1"
    ):


        try:


            result = self.session.get_kline(

                category=CATEGORY,

                symbol=DEFAULT_SYMBOL,

                interval=interval,

                limit=200

            )


            return result



        except Exception as e:


            print(
                "[KLINE ERROR]",
                e
            )


            return None




    # ==================================================
    # ORDER
    # ==================================================

    def create_order(
        self,
        side,
        qty
    ):


        try:


            result = self.session.place_order(

                category=CATEGORY,

                symbol=DEFAULT_SYMBOL,

                side=side,

                orderType="Market",

                qty=str(qty),

                timeInForce="GTC"

            )


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




    # ==================================================
    # SERVER TIME
    # ==================================================

    def server_time(self):

        return int(
            time.time()*1000
        )




# singleton

bybit_api = BybitAPI()
