# api/bybit_api.py

import time

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

            api_key=BYBIT_API_KEY,

            api_secret=BYBIT_API_SECRET

        )



    # ==================================
    # CONNECTION TEST
    # ==================================

    def ping(self):


        try:


            result = self.session.get_server_time()


            if result.get(
                "retCode"
            ) == 0:


                return True



            return False



        except Exception as e:


            print(
                "[PING ERROR]",
                e
            )


            return False





    # ==================================
    # WALLET
    # ==================================

    def get_wallet_balance(self):


        try:


            response = (
                self.session
                .get_wallet_balance(

                    accountType="UNIFIED"

                )
            )


            if response.get(
                "retCode"
            ) != 0:


                print(
                    "[WALLET ERROR]",
                    response
                )


                return None



            return response



        except Exception as e:


            print(
                "[WALLET EXCEPTION]",
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


            if result.get(
                "retCode"
            ) == 0:


                print(
                    "[LEVERAGE SET]",
                    LEVERAGE
                )


                return True



            return False



        except Exception as e:


            msg = str(e)



            if "110043" in msg:


                print(
                    "[LEVERAGE OK] already set"
                )


                return True



            print(
                "[LEVERAGE ERROR]",
                e
            )


            return False





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



            if result.get(
                "retCode"
            ) != 0:


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
    # MARKET ORDER
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


            positions = (

                self.session
                .get_positions(

                    category=CATEGORY,

                    symbol=DEFAULT_SYMBOL

                )

            )


            pos = (

                positions
                ["result"]
                ["list"][0]

            )



            size = float(
                pos["size"]
            )



            if size == 0:


                return True



            side = (

                "Sell"
                if pos["side"] == "Buy"
                else "Buy"

            )



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
# SINGLETON
# ==================================

bybit_api = BybitAPI()
