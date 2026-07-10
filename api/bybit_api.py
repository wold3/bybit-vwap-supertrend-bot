import time


from pybit.unified_trading import HTTP



from config import (

    BYBIT_API_KEY,

    BYBIT_API_SECRET,

    BYBIT_TESTNET,

    BYBIT_DEMO,

    BYBIT_BASE_URL,

    CATEGORY,

    DEFAULT_SYMBOL,

    ACCOUNT_TYPE,

    DEFAULT_QTY,

    ORDER_TYPE,

    TIME_IN_FORCE,

    LEVERAGE

)





# ==========================================
# BYBIT API CLIENT
# ==========================================

class BybitAPI:


    def __init__(self):


        print("==============================")
        print("[BYBIT API INIT]")
        print("BASE :", BYBIT_BASE_URL)
        print("TESTNET :", BYBIT_TESTNET)
        print("DEMO :", BYBIT_DEMO)
        print("ACCOUNT :", ACCOUNT_TYPE)
        print("CATEGORY :", CATEGORY)
        print("SYMBOL :", DEFAULT_SYMBOL)
        print("==============================")




        self.session = HTTP(


            testnet=BYBIT_TESTNET,


            demo=BYBIT_DEMO,


            api_key=BYBIT_API_KEY,


            api_secret=BYBIT_API_SECRET


        )





    # ======================================
    # WALLET
    # ======================================

    def get_wallet_balance(self):


        try:


            response = self.session.get_wallet_balance(


                accountType=ACCOUNT_TYPE


            )


            print(
                "[WALLET RESPONSE]"
            )


            return response




        except Exception as e:


            print(
                "[WALLET ERROR]",
                e
            )


            return None





    # ======================================
    # POSITION
    # ======================================

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





    # ======================================
    # KLINE
    # ======================================

    def get_kline(

        self,

        interval="1",

        limit=200

    ):


        try:


            return self.session.get_kline(


                category=CATEGORY,


                symbol=DEFAULT_SYMBOL,


                interval=interval,


                limit=limit


            )




        except Exception as e:


            print(
                "[KLINE ERROR]",
                e
            )


            return None





    # ======================================
    # TICKER
    # ======================================

    def get_price(self):


        try:


            result = self.session.get_tickers(


                category=CATEGORY,


                symbol=DEFAULT_SYMBOL


            )



            price = result["result"]["list"][0]["lastPrice"]



            return float(price)




        except Exception as e:


            print(
                "[PRICE ERROR]",
                e
            )


            return None





    # ======================================
    # LEVERAGE
    # ======================================

    def set_leverage(self):


        try:


            result = self.session.set_leverage(


                category=CATEGORY,


                symbol=DEFAULT_SYMBOL,


                buyLeverage=str(LEVERAGE),


                sellLeverage=str(LEVERAGE)


            )



            print(
                "[LEVERAGE SET]",
                result
            )



            return True




        except Exception as e:


            msg = str(e)



            if "110043" in msg:


                print(
                    "[LEVERAGE ALREADY SET]"
                )


                return True




            print(
                "[LEVERAGE ERROR]",
                e
            )


            return False





    # ======================================
    # CREATE ORDER
    # ======================================

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



            print(
                "[ORDER RESPONSE]"
            )


            print(response)



            return response




        except Exception as e:


            print(
                "[ORDER ERROR]",
                e
            )


            return None





    # ======================================
    # CANCEL
    # ======================================

    def cancel_all_orders(self):


        try:


            return self.session.cancel_all_orders(


                category=CATEGORY,


                symbol=DEFAULT_SYMBOL


            )




        except Exception as e:


            print(
                "[CANCEL ERROR]",
                e
            )


            return None





    # ======================================
    # ORDER HISTORY
    # ======================================

    def get_open_orders(self):


        try:


            return self.session.get_open_orders(


                category=CATEGORY,


                symbol=DEFAULT_SYMBOL


            )



        except Exception as e:


            print(
                "[OPEN ORDER ERROR]",
                e
            )


            return None





    # ======================================
    # SERVER TIME
    # ======================================

    def server_time(self):


        return int(

            time.time()*1000

        )





# ==========================================
# SINGLETON
# ==========================================

bybit_api = BybitAPI()
