# =====================================================
# api/bybit_api.py
# Bybit V5 API Wrapper
# Demo / Live Support
# =====================================================

from pybit.unified_trading import HTTP


from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    LIVE,
    CATEGORY,
    DEFAULT_SYMBOL,
    LEVERAGE
)





class BybitAPI:


    def __init__(self):


        self.session = HTTP(

            testnet=False,

            demo=not LIVE,

            api_key=BYBIT_API_KEY,

            api_secret=BYBIT_API_SECRET

        )



        print(

            "[BYBIT API READY]",

            "LIVE" if LIVE else "DEMO"

        )









    # =====================================================
    # KLINE
    # =====================================================


    def get_kline(
        self,
        limit=200
    ):


        try:


            result = self.session.get_kline(


                category=CATEGORY,


                symbol=DEFAULT_SYMBOL,


                interval="5",


                limit=limit


            )



            if result.get("retCode") != 0:


                print(

                    "[KLINE ERROR]",

                    result

                )


                return []





            return (

                result

                ["result"]

                ["list"]

            )






        except Exception as e:


            print(

                "[KLINE EXCEPTION]",

                e

            )


            return []









    # =====================================================
    # MARKET ORDER
    # =====================================================


    def place_order(
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


                leverage=str(LEVERAGE)


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
    # POSITION
    # =====================================================


    def get_position(self):


        try:


            return self.session.get_positions(


                category=CATEGORY,


                symbol=DEFAULT_SYMBOL


            )





        except Exception as e:


            print(

                "[POSITION ERROR]",

                e

            )


            return None










    # =====================================================
    # TP / SL
    # =====================================================


    def set_trading_stop(
        self,
        tp,
        sl
    ):


        try:


            result = self.session.set_trading_stop(


                category=CATEGORY,


                symbol=DEFAULT_SYMBOL,


                takeProfit=str(tp),


                stopLoss=str(sl)


            )



            print(

                "[TP SL RESULT]",

                result

            )



            return result





        except Exception as e:


            print(

                "[TP SL ERROR]",

                e

            )


            return None










    # =====================================================
    # WALLET
    # =====================================================


    def get_balance(self):


        try:


            result = self.session.get_wallet_balance(


                accountType="UNIFIED"


            )



            return result





        except Exception as e:


            print(

                "[BALANCE ERROR]",

                e

            )


            return None










# =====================================================
# INSTANCE
# =====================================================


bybit_api = BybitAPI()
