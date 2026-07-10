# api/bybit_api.py

from pybit.unified_trading import HTTP

from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,

    BYBIT_TESTNET,
    BYBIT_DEMO,

    CATEGORY,
    DEFAULT_SYMBOL,

    LEVERAGE
)



class BybitAPI:


    def __init__(self):

        print("==============================")
        print("[BYBIT API INIT]")
        print("TESTNET :", BYBIT_TESTNET)
        print("DEMO    :", BYBIT_DEMO)
        print("ACCOUNT : UNIFIED")
        print("CATEGORY:", CATEGORY)
        print("SYMBOL  :", DEFAULT_SYMBOL)
        print("==============================")


        self.session = HTTP(

            testnet=BYBIT_TESTNET,

            demo=BYBIT_DEMO,

            api_key=BYBIT_API_KEY,

            api_secret=BYBIT_API_SECRET

        )



    # ==================================
    # PING
    # ==================================

    def ping(self):

        try:

            result = (
                self.session
                .get_server_time()
            )


            if result.get("retCode") == 0:

                return True


            return False



        except Exception as e:

            print(
                "[PING ERROR]",
                e
            )

            return False



    # ==================================
    # WALLET BALANCE
    # ==================================

    def get_wallet_balance(self):

        try:

            result = (

                self.session
                .get_wallet_balance(

                    accountType="UNIFIED"

                )

            )


            if result.get("retCode") != 0:

                print(
                    "[WALLET ERROR]",
                    result
                )

                return None



            return result



        except Exception as e:

            print(
                "[WALLET EXCEPTION]",
                e
            )

            return None



    # ==================================
    # KLINE
    # ==================================

    def get_kline(
        self,
        interval="1"
    ):

        try:


            result = (

                self.session
                .get_kline(

                    category=CATEGORY,

                    symbol=DEFAULT_SYMBOL,

                    interval=interval,

                    limit=200

                )

            )


            if result.get("retCode") != 0:

                print(
                    "[KLINE ERROR]",
                    result
                )

                return None



            rows = (

                result
                ["result"]
                ["list"]

            )


            candles = []


            for row in reversed(rows):

                candles.append(

                    {

                        "timestamp":
                            int(row[0]),


                        "open":
                            float(row[1]),


                        "high":
                            float(row[2]),


                        "low":
                            float(row[3]),


                        "close":
                            float(row[4]),


                        "volume":
                            float(row[5])

                    }

                )


            return candles



        except Exception as e:


            print(
                "[KLINE EXCEPTION]",
                e
            )


            return None



    # ==================================
    # LEVERAGE
    # ==================================

    def set_leverage(self):

        try:


            result = (

                self.session
                .set_leverage(

                    category=CATEGORY,

                    symbol=DEFAULT_SYMBOL,

                    buyLeverage=str(
                        LEVERAGE
                    ),

                    sellLeverage=str(
                        LEVERAGE
                    )

                )

            )


            if result.get("retCode") == 0:

                print(
                    "[LEVERAGE SET]",
                    LEVERAGE
                )

                return True



            return False



        except Exception as e:


            error = str(e)



            # 이미 설정된 경우 정상 처리

            if "110043" in error:


                print(
                    "[LEVERAGE ALREADY SET]"
                )

                return True



            print(
                "[LEVERAGE ERROR]",
                e
            )


            return False



    # ==================================
    # LAST PRICE
    # ==================================

    def get_last_price(self):

        try:


            result = (

                self.session
                .get_tickers(

                    category=CATEGORY,

                    symbol=DEFAULT_SYMBOL

                )

            )


            return float(

                result
                ["result"]
                ["list"][0]
                ["lastPrice"]

            )



        except Exception as e:


            print(
                "[PRICE ERROR]",
                e
            )


            return None



    # ==================================
    # CREATE ORDER
    # ==================================

    def create_order(
        self,
        side,
        qty
    ):

        try:


            result = (

                self.session
                .place_order(

                    category=CATEGORY,

                    symbol=DEFAULT_SYMBOL,

                    side=side,

                    orderType="Market",

                    qty=str(qty)

                )

            )


            return result



        except Exception as e:


            print(
                "[ORDER ERROR]",
                e
            )


            return None



    # ==================================
    # CLOSE POSITION
    # ==================================

    def close_position(self):

        try:


            result = (

                self.session
                .get_positions(

                    category=CATEGORY,

                    symbol=DEFAULT_SYMBOL

                )

            )


            position = (

                result
                ["result"]
                ["list"][0]

            )


            size = float(
                position["size"]
            )


            if size == 0:

                return True



            if position["side"] == "Buy":

                side = "Sell"

            else:

                side = "Buy"



            return self.create_order(

                side,

                size

            )



        except Exception as e:


            print(
                "[CLOSE ERROR]",
                e
            )


            return False



    # ==================================
    # POSITION
    # ==================================

    def get_position(self):

        try:


            return (

                self.session
                .get_positions(

                    category=CATEGORY,

                    symbol=DEFAULT_SYMBOL

                )

            )



        except Exception as e:


            print(
                "[POSITION ERROR]",
                e
            )


            return None





# Singleton

bybit_api = BybitAPI()
