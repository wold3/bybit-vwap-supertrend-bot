# =====================================================
# api/bybit_api.py
# VWAP SUPERTREND BOT V3
# BYBIT V5 API MANAGER
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

    get_trading_symbol,

    add_log

)








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


                demo=(mode=="DEMO"),


                api_key=key,


                api_secret=secret


            )



            self.current_mode = mode




            add_log(

                f"BYBIT SESSION {mode}"

            )









    def check_session(self):


        if get_trading_mode()!=self.current_mode:


            self.create_session()












    # =====================================================
    # SYMBOL
    # =====================================================


    def sync_symbol(self):


        try:


            symbol=get_trading_symbol()



            if symbol != self.symbol:


                self.symbol=symbol.upper()



                add_log(

                    f"SYMBOL {self.symbol}"

                )



        except:


            pass







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


            self.sync_symbol()



            return self.session.get_kline(


                category=CATEGORY,


                symbol=self.symbol,


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


            self.sync_symbol()



            result=self.session.get_tickers(


                category=CATEGORY,


                symbol=self.symbol


            )



            return float(

                result["result"]["list"][0]["lastPrice"]

            )



        except Exception as e:


            add_log(

                f"PRICE ERROR {e}"

            )


            return 0












    # =====================================================
    # LEVERAGE
    # =====================================================


    def set_leverage(self):


        try:


            self.check_session()


            self.sync_symbol()



            leverage=int(LEVERAGE)



            if leverage>100:


                leverage=100






            return self.session.set_leverage(


                category=CATEGORY,


                symbol=self.symbol,


                buyLeverage=str(leverage),


                sellLeverage=str(leverage)



            )




        except Exception as e:


            error=str(e)



            if (

                "110043" in error

                or

                "not modified" in error.lower()

            ):



                add_log(

                    f"LEVERAGE {LEVERAGE}X ALREADY"

                )


                return True




            add_log(

                f"LEVERAGE ERROR {error}"

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


            self.sync_symbol()



            qty=float(qty)



            result=self.session.place_order(


                category=CATEGORY,


                symbol=self.symbol,


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


            self.sync_symbol()



            return self.session.get_positions(


                category=CATEGORY,


                symbol=self.symbol


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


            return self.session.get_wallet_balance(


                accountType="UNIFIED"


            )



        except Exception as e:


            add_log(

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


            self.sync_symbol()



            params={


                "category":CATEGORY,


                "symbol":self.symbol


            }



            if tp:


                params["takeProfit"]=str(tp)



            if sl:


                params["stopLoss"]=str(sl)







            return self.session.set_trading_stop(

                **params

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


            pos=self.get_position()



            rows=pos.get(

                "result",

                {}

            ).get(

                "list",

                []

            )



            if not rows:


                return False






            p=rows[0]



            size=float(

                p.get(

                    "size",

                    0

                )

            )



            if size<=0:


                return False





            side=p.get(

                "side"

            )




            close_side=(

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


            add_log(

                f"CLOSE ERROR {e}"

            )


            return None











# =====================================================
# INSTANCE
# =====================================================


bybit_api = BybitAPI()
