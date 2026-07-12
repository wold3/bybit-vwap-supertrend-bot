# =====================================================
# api/bybit_api.py
# VWAP SUPERTREND BOT
# BYBIT V5 API MANAGER
# DEMO / LIVE
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





def log(msg):

    try:

        from web.server import add_log

        add_log(msg)

    except:

        print(msg)







def trading_mode():

    try:

        from web.server import get_trading_mode

        return get_trading_mode()


    except:

        return "DEMO"








class BybitAPI:



    def __init__(self):


        self.session = None


        self.current_mode = None


        self.symbol = SYMBOL


        self.lock = threading.Lock()



        self.create_session()








    # =====================================================
    # SESSION
    # =====================================================

    def create_session(self):


        mode = trading_mode()



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


                demo=(mode=="DEMO"),


                api_key=key,


                api_secret=secret


            )



            self.current_mode = mode



            print(

                "[BYBIT SESSION]",

                mode

            )


            log(

                f"BYBIT SESSION {mode}"

            )










    def check_session(self):


        if trading_mode()!=self.current_mode:


            self.create_session()











    # =====================================================
    # SYMBOL
    # =====================================================

    def change_symbol(self,symbol):


        self.symbol = symbol.upper()


        log(

            f"SYMBOL {self.symbol}"

        )


        return True










    # =====================================================
    # KLINE
    # =====================================================

    def get_kline(

        self,

        interval="5",

        limit=100

    ):


        try:


            self.check_session()



            return self.session.get_kline(

                category=CATEGORY,

                symbol=self.symbol,

                interval=str(interval),

                limit=limit

            )



        except Exception as e:


            log(

                f"KLINE ERROR {e}"

            )


            return None










    # =====================================================
    # PRICE
    # =====================================================

    def get_price(self):


        try:


            self.check_session()



            r=self.session.get_tickers(

                category=CATEGORY,

                symbol=self.symbol

            )



            return float(

                r["result"]["list"][0]["lastPrice"]

            )



        except Exception as e:


            log(

                f"PRICE ERROR {e}"

            )


            return 0










    # =====================================================
    # LEVERAGE
    # =====================================================

    def set_leverage(self):


        try:


            self.check_session()



            return self.session.set_leverage(


                category=CATEGORY,


                symbol=self.symbol,


                buyLeverage=str(LEVERAGE),


                sellLeverage=str(LEVERAGE)


            )



        except Exception as e:


            if "110043" in str(e):


                return True



            log(

                f"LEVERAGE ERROR {e}"

            )


            return False










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



            result=self.session.place_order(



                category=CATEGORY,


                symbol=self.symbol,


                side=side,


                orderType="Market",


                qty=str(qty),


                reduceOnly=reduce_only



            )



            log(

                f"ORDER {side} {qty}"

            )


            return result





        except Exception as e:


            log(

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


                symbol=self.symbol


            )



        except Exception as e:


            log(

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


            log(

                f"BALANCE ERROR {e}"

            )


            return None










    # =====================================================
    # TP / SL
    # =====================================================

    def set_trading_stop(

        self,

        tp=None,

        sl=None

    ):


        try:


            self.check_session()



            params={


                "category":CATEGORY,


                "symbol":self.symbol



            }



            if tp:

                params["takeProfit"]=str(tp)



            if sl:

                params["stopLoss"]=str(sl)





            result=self.session.set_trading_stop(

                **params

            )



            log(

                f"TP {tp} SL {sl}"

            )



            return result





        except Exception as e:


            log(

                f"TP SL ERROR {e}"

            )


            return None










    # =====================================================
    # CLOSE POSITION
    # =====================================================

    def close_position(self):


        try:


            data=self.get_position()



            rows=data["result"]["list"]



            if not rows:

                return None




            pos=rows[0]



            size=float(

                pos["size"]

            )



            if size<=0:

                return None




            side=pos["side"]



            close_side = (

                "Sell"

                if side=="Buy"

                else

                "Buy"

            )




            return self.place_order(

                close_side,

                size,

                True

            )



        except Exception as e:


            log(

                f"CLOSE ERROR {e}"

            )


            return None










    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "mode":

            self.current_mode,


            "symbol":

            self.symbol


        }








# =====================================================
# INSTANCE
# =====================================================

bybit_api = BybitAPI()
