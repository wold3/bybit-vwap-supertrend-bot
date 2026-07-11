# =====================================================
# api/bybit_api.py
# VWAP SUPERTREND BOT
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

    get_trading_mode,

    add_log

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





            if mode == "DEMO":


                key = DEMO_API_KEY

                secret = DEMO_API_SECRET



            else:


                key = LIVE_API_KEY

                secret = LIVE_API_SECRET





            self.session = HTTP(


                testnet=False,


                demo=(mode == "DEMO"),


                api_key=key,


                api_secret=secret


            )



            self.current_mode = mode



            print(

                "[BYBIT READY]",

                mode

            )


            add_log(

                f"BYBIT SESSION {mode}"

            )







    # =====================================================
    # SESSION CHECK
    # =====================================================

    def check_session(self):


        if get_trading_mode() != self.current_mode:


            self.create_session()







    # =====================================================
    # CHANGE SESSION
    # =====================================================

    def change_session(self, mode):


        with self.lock:

            self.current_mode = None


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



            return self.session.get_kline(


                category=CATEGORY,


                symbol=SYMBOL,


                interval=str(interval),


                limit=limit


            )




        except Exception as e:


            add_log(

                f"KLINE ERROR {e}"

            )


            return None







    # =====================================================
    # PRICE
    # =====================================================

    def get_price(self):


        try:


            self.check_session()



            result = self.session.get_tickers(


                category=CATEGORY,


                symbol=SYMBOL


            )



            return float(

                result["result"]["list"][0]["lastPrice"]

            )




        except Exception as e:


            add_log(

                f"PRICE ERROR {e}"

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


                symbol=SYMBOL,


                buyLeverage=str(LEVERAGE),


                sellLeverage=str(LEVERAGE)


            )



        except Exception as e:


            add_log(

                f"LEVERAGE ERROR {e}"

            )


            return None







    # =====================================================
    # ORDER
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


                symbol=SYMBOL,


                side=side,


                orderType="Market",


                qty=str(qty),


                reduceOnly=reduce_only



            )



            add_log(

                f"ORDER {side} {qty}"

            )


            return result




        except Exception as e:


            add_log(

                f"ORDER ERROR {e}"

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


                symbol=SYMBOL


            )



        except Exception as e:


            add_log(

                f"POSITION ERROR {e}"

            )


            return None








    # =====================================================
    # BALANCE
    # =====================================================

    def get_balance(self):


        try:


            self.check_session()



            return self.session.get_wallet_balance(


                accountType="UNIFIED"


            )




        except Exception as e:


            add_log(

                f"BALANCE ERROR {e}"

            )


            return None







    # =====================================================
    # TP SL
    # =====================================================

    def set_trading_stop(

        self,

        tp,

        sl

    ):


        try:


            self.check_session()



            return self.session.set_trading_stop(


                category=CATEGORY,


                symbol=SYMBOL,


                takeProfit=str(tp),


                stopLoss=str(sl)


            )



        except Exception as e:


            add_log(

                f"TP SL ERROR {e}"

            )


            return None







    # =====================================================
    # CLOSE POSITION
    # =====================================================

    def close_position(self):


        try:


            pos = self.get_position()



            if not pos:

                return None




            rows = pos["result"]["list"]



            if not rows:

                return None




            p = rows[0]



            size = float(

                p.get(

                    "size",

                    0

                )

            )



            if size <= 0:

                return None




            side = p.get(

                "side",

                ""

            )



            if side == "Buy":


                close_side = "Sell"



            elif side == "Sell":


                close_side = "Buy"



            else:


                return None




            return self.place_order(


                close_side,


                size,


                True


            )




        except Exception as e:


            add_log(

                f"CLOSE ERROR {e}"

            )


            return None






# =====================================================
# INSTANCE
# =====================================================

bybit_api = BybitAPI()
