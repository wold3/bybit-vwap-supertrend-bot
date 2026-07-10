import time

from pybit.unified_trading import HTTP


from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    BYBIT_TESTNET,
    BYBIT_BASE_URL,

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
        print("BASE :", BYBIT_BASE_URL)
        print("TESTNET :", BYBIT_TESTNET)
        print("ACCOUNT :", ACCOUNT_TYPE)
        print("CATEGORY :", CATEGORY)
        print("SYMBOL :", DEFAULT_SYMBOL)
        print("==============================")


        self.session = HTTP(

            testnet=BYBIT_TESTNET,

            api_key=BYBIT_API_KEY,

            api_secret=BYBIT_API_SECRET

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

        interval="1",

        limit=200

    ):


        try:


            result = self.session.get_kline(

                category=CATEGORY,

                symbol=DEFAULT_SYMBOL,

                interval=interval,

                limit=limit

            )


            return result



        except Exception as e:


            print(
                "[KLINE ERROR]",
                e
            )


            return None





    # ==================================================
    # MARKET ORDER
    # ==================================================

    def create_order(

        self,

        side,

        qty=None

    ):


        try:


            if qty is None:

                qty = DEFAULT_QTY



            result = self.session.place_order(

                category=CATEGORY,

                symbol=DEFAULT_SYMBOL,

                side=side,

                orderType=ORDER_TYPE,

                qty=str(qty),

                timeInForce=TIME_IN_FORCE

            )


            print("[ORDER RESPONSE]")

            print(result)



            return result



        except Exception as e:


            print(
                "[ORDER ERROR]",
                e
            )


            return None





    # ==================================================
    # CANCEL ALL ORDER
    # ==================================================

    def cancel_all_orders(self):


        try:


            result = self.session.cancel_all_orders(

                category=CATEGORY,

                symbol=DEFAULT_SYMBOL

            )


            print(
                "[CANCEL ALL]"
            )


            return result



        except Exception as e:


            print(
                "[CANCEL ERROR]",
                e
            )


            return None





    # ==================================================
    # SET LEVERAGE
    # ==================================================

    def set_leverage(

        self,

        leverage=LEVERAGE

    ):


        try:


            result = self.session.set_leverage(

                category=CATEGORY,

                symbol=DEFAULT_SYMBOL,

                buyLeverage=str(leverage),

                sellLeverage=str(leverage)

            )


            print("[LEVERAGE RESPONSE]")

            print(result)


            return result



        except Exception as e:


            print(
                "[LEVERAGE ERROR]",
                e
            )


            return None





    # ==================================================
    # SET TP / SL
    # ==================================================

    def set_trading_stop(

        self,

        take_profit,

        stop_loss

    ):


        try:


            result = self.session.set_trading_stop(

                category=CATEGORY,

                symbol=DEFAULT_SYMBOL,

                tpslMode="Full",

                positionIdx=0,

                takeProfit=str(take_profit),

                stopLoss=str(stop_loss)

            )


            print("[TP SL RESPONSE]")

            print(result)


            return result



        except Exception as e:


            print(
                "[TP SL ERROR]",
                e
            )


            return None





    # ==================================================
    # CLOSE POSITION
    # ==================================================

    def close_position(self):


        try:


            position = self.get_position()



            if position is None:

                return None



            data = position["result"]["list"]



            for p in data:


                size = float(

                    p.get(
                        "size",
                        0

                    )

                )


                if size <= 0:

                    continue



                side = p["side"]



                close_side = (

                    "Sell"

                    if side == "Buy"

                    else

                    "Buy"

                )



                result = self.create_order(

                    side=close_side,

                    qty=size

                )


                return result




            return None




        except Exception as e:


            print(
                "[CLOSE ERROR]",
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





# ==================================================
# SINGLETON
# ==================================================

bybit_api = BybitAPI()
