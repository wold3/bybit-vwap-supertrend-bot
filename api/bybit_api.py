# =====================================================
# api/bybit_api.py
# Bybit V5 API Manager
# Demo / Live Dynamic Switch
# =====================================================

from pybit.unified_trading import HTTP

import threading



from config import (

    BYBIT_API_KEY,

    BYBIT_API_SECRET,

    CATEGORY,

    DEFAULT_SYMBOL

)





from web.server import (

    get_trading_mode

)







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


                self.session = HTTP(


                    testnet=False,


                    demo=True,


                    api_key=BYBIT_API_KEY,


                    api_secret=BYBIT_API_SECRET


                )





            else:


                self.session = HTTP(


                    testnet=False,


                    demo=False,


                    api_key=BYBIT_API_KEY,


                    api_secret=BYBIT_API_SECRET


                )





            self.current_mode = mode





            print(

                "[BYBIT READY]",

                mode

            )









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

        limit=200

    ):


        try:


            self.check_session()



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





            return result["result"]["list"]





        except Exception as e:


            print(

                "[KLINE ERROR]",

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


            self.check_session()



            result = self.session.place_order(


                category=CATEGORY,


                symbol=DEFAULT_SYMBOL,


                side=side,


                orderType="Market",


                qty=str(qty)


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





            item = position["result"]["list"][0]



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

                size

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
