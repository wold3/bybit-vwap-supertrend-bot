# =====================================================
# api/bybit_api.py
# Bybit V5 API Manager
# Demo / Live Dynamic Switch
# =====================================================

from pybit.unified_trading import HTTP

import threading


from config import (

    DEMO_API_KEY,
    DEMO_API_SECRET,

    LIVE_API_KEY,
    LIVE_API_SECRET,

    CATEGORY,
    SYMBOL,
    LEVERAGE

)


from web.server import (

    get_trading_mode

)



DEFAULT_SYMBOL = SYMBOL



class BybitAPI:


    def __init__(self):

        self.session = None

        self.current_mode = None

        self.lock = threading.Lock()

        self.create_session()



    # =====================================================
    # CREATE SESSION
    # =====================================================

    def create_session(self):

        mode = get_trading_mode()


        with self.lock:


            if mode == self.current_mode:

                return



            print(

                "[BYBIT SESSION CHANGE]",

                mode

            )



            if mode == "DEMO":

                api_key = DEMO_API_KEY

                api_secret = DEMO_API_SECRET


            else:

                api_key = LIVE_API_KEY

                api_secret = LIVE_API_SECRET



            self.session = HTTP(

                testnet=False,

                demo=(mode == "DEMO"),

                api_key=api_key,

                api_secret=api_secret

            )



            self.current_mode = mode



            print(

                "[BYBIT READY]",

                mode

            )



    # =====================================================
    # CHANGE SESSION
    # =====================================================

    def change_session(

        self,

        mode

    ):


        with self.lock:


            self.current_mode = None



        self.create_session()



    # =====================================================
    # CHECK SESSION
    # =====================================================

    def check_session(self):


        if get_trading_mode() != self.current_mode:

            self.create_session()



    # =====================================================
    # KLINE
    # =====================================================

    def get_kline(

        self,

        interval="5",

        limit=200

    ):


        try:

            self.check_session()



            result = self.session.get_kline(

                category=CATEGORY,

                symbol=DEFAULT_SYMBOL,

                interval=interval,

                limit=limit

            )



            if result.get("retCode") != 0:


                print(

                    "[KLINE ERROR]",

                    result

                )


                return []



            return result



        except Exception as e:


            print(

                "[KLINE ERROR]",

                e

            )


            return []



    # =====================================================
    # PRICE
    # =====================================================

    def get_price(self):


        try:


            self.check_session()



            result = self.session.get_tickers(

                category=CATEGORY,

                symbol=DEFAULT_SYMBOL

            )



            if result.get("retCode") != 0:

                return None



            price = (

                result["result"]

                ["list"][0]

                ["lastPrice"]

            )


            return float(price)



        except Exception as e:


            print(

                "[PRICE ERROR]",

                e

            )


            return None



    # =====================================================
    # LEVERAGE
    # =====================================================

    def set_leverage(self):


        try:


            self.check_session()



            return self.session.set_leverage(

                category=CATEGORY,

                symbol=DEFAULT_SYMBOL,

                buyLeverage=str(LEVERAGE),

                sellLeverage=str(LEVERAGE)

            )



        except Exception as e:


            print(

                "[LEVERAGE ERROR]",

                e

            )


            return None



    # =====================================================
    # MARKET ORDER
    # =====================================================

    def place_order(

        self,

        side,

        qty,

        reduce_only=False

    ):


        try:


            self.check_session()



            result = self.session.place_order(

                category=CATEGORY,

                symbol=DEFAULT_SYMBOL,

                side=side,

                orderType="Market",

                qty=str(qty),

                reduceOnly=reduce_only

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


            self.check_session()



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
    # WALLET BALANCE
    # =====================================================

    def get_balance(self):


        try:


            self.check_session()



            result = self.session.get_wallet_balance(

                accountType="UNIFIED"

            )



            if result.get("retCode") != 0:


                print(

                    "[BALANCE ERROR]",

                    result

                )


                return None



            return result



        except Exception as e:


            print(

                "[BALANCE ERROR]",

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


            self.check_session()



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
    # CLOSE POSITION
    # =====================================================

    def close_position(self):


        try:


            position = self.get_position()



            if not position:

                return None



            rows = position["result"]["list"]



            if not rows:

                return None



            item = rows[0]



            size = float(

                item.get(

                    "size",

                    0

                )

            )



            if size <= 0:

                return None



            side = item.get(

                "side"

            )



            close_side = (

                "Sell"

                if side == "Buy"

                else

                "Buy"

            )



            return self.place_order(

                close_side,

                size,

                reduce_only=True

            )



        except Exception as e:


            print(

                "[CLOSE ERROR]",

                e

            )


            return None



# =====================================================
# INSTANCE
# =====================================================

bybit_api = BybitAPI()
