# =====================================================
# api/bybit_api.py
# Bybit V5 Unified API Wrapper
# =====================================================

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







    # =====================================================
    # PING
    # =====================================================

    def ping(self):

        try:

            result = (
                self.session
                .get_server_time()
            )


            return (

                result.get(
                    "retCode"
                )

                ==

                0

            )


        except Exception as e:


            print(
                "[PING ERROR]",
                e
            )


            return False







    # =====================================================
    # WALLET
    # =====================================================

    def get_wallet_balance(self):


        try:


            result = (

                self.session
                .get_wallet_balance(

                    accountType="UNIFIED"

                )

            )


            if result.get(
                "retCode"
            ) != 0:


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







    # =====================================================
    # KLINE
    # =====================================================

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

                        int(
                            row[0]
                        ),


                    "open":

                        float(
                            row[1]
                        ),


                    "high":

                        float(
                            row[2]
                        ),


                    "low":

                        float(
                            row[3]
                        ),


                    "close":

                        float(
                            row[4]
                        ),


                    "volume":

                        float(
                            row[5]
                        )


                    }

                )



            print(
                "[KLINE]",
                len(candles)
            )


            return candles




        except Exception as e:


            print(
                "[KLINE ERROR]",
                e
            )


            return None







    # =====================================================
    # LEVERAGE
    # =====================================================

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
                    "[LEVERAGE SET]"
                )


                return True



            return False




        except Exception as e:


            if "110043" in str(e):


                print(
                    "[LEVERAGE ALREADY SET]"
                )


                return True



            print(
                "[LEVERAGE ERROR]",
                e
            )


            return False







    # =====================================================
    # PRICE
    # =====================================================

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







    # =====================================================
    # CREATE ORDER
    # =====================================================

    def create_order(
        self,
        side,
        qty,
        stop_loss=None,
        take_profit=None,
        reduce_only=False
    ):


        try:


            params = {


                "category":

                    CATEGORY,


                "symbol":

                    DEFAULT_SYMBOL,


                "side":

                    side,


                "orderType":

                    "Market",


                "qty":

                    str(qty),


                "positionIdx":

                    0


            }



            if stop_loss:


                params["stopLoss"] = str(
                    stop_loss
                )



            if take_profit:


                params["takeProfit"] = str(
                    take_profit
                )



            if reduce_only:


                params["reduceOnly"] = True






            result = (

                self.session
                .place_order(

                    **params

                )

            )



            print(
                "[ORDER RESULT]",
                result
            )



            return result




        except Exception as e:


            print(
                "[ORDER ERROR]",
                e
            )


            return None







    # =====================================================
    # CLOSE POSITION
    # =====================================================

    def close_position(self):


        try:


            position = (

                self.get_position()

            )



            rows = (

                position
                ["result"]
                ["list"]

            )



            for p in rows:


                size = float(

                    p.get(
                        "size",
                        0
                    )

                )



                if size <= 0:

                    continue



                if p["side"] == "Buy":

                    side = "Sell"


                else:

                    side = "Buy"





                return self.create_order(

                    side,

                    size,

                    reduce_only=True

                )




            return True



        except Exception as e:


            print(
                "[CLOSE ERROR]",
                e
            )


            return False







    # =====================================================
    # POSITION
    # =====================================================

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







# =====================================================
# SINGLETON
# =====================================================

bybit_api = BybitAPI()
