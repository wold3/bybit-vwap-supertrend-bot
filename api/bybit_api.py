# =====================================================
# api/bybit_api.py
# VWAP SUPERTREND BOT
# BYBIT V5 API MANAGER
# DEMO / LIVE + DYNAMIC SYMBOL
# =====================================================

from pybit.unified_trading import HTTP

import threading

import config


from web.server import (
    get_trading_mode,
    add_log,
    update_status
)





class BybitAPI:


    def __init__(self):

        self.session = None

        self.current_mode = None

        self.symbol = config.SYMBOL

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


                key = config.DEMO_API_KEY

                secret = config.DEMO_API_SECRET



            else:


                key = config.LIVE_API_KEY

                secret = config.LIVE_API_SECRET






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



            add_log(

                f"BYBIT SESSION {mode}"

            )






    def check_session(self):


        if get_trading_mode() != self.current_mode:

            self.create_session()







    # =====================================================
    # SYMBOL
    # =====================================================


    def change_symbol(self,symbol):


        self.symbol = symbol.upper()



        config.SYMBOL = self.symbol



        add_log(

            f"SYMBOL CHANGE {self.symbol}"

        )



        update_status({

            "symbol":

                self.symbol,


            "last_action":

                f"SYMBOL {self.symbol}"

        })



        return True







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


                category=config.CATEGORY,


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



            result=self.session.get_tickers(


                category=config.CATEGORY,


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



            return self.session.set_leverage(


                category=config.CATEGORY,


                symbol=self.symbol,


                buyLeverage=str(config.LEVERAGE),


                sellLeverage=str(config.LEVERAGE)



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



            result=self.session.place_order(


                category=config.CATEGORY,


                symbol=self.symbol,


                side=side,


                orderType="Market",


                qty=str(qty),


                reduceOnly=reduce_only



            )



            add_log(

                f"ORDER {self.symbol} {side} {qty}"

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


                category=config.CATEGORY,


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


                category=config.CATEGORY,


                symbol=self.symbol,


                takeProfit=str(tp),


                stopLoss=str(sl)


            )



        except Exception as e:


            add_log(

                f"TP SL ERROR {e}"

            )


            return None







    # =====================================================
    # CLOSE
    # =====================================================


    def close_position(self):


        try:


            position=self.get_position()



            if not position:

                return None




            rows=(

                position

                .get("result",{})

                .get("list",[])

            )



            if not rows:

                return None




            p=rows[0]



            size=float(

                p.get(

                    "size",

                    0

                )

                or 0

            )



            if size<=0:

                return None




            side=p.get(

                "side",

                ""

            )




            if side=="Buy":


                close_side="Sell"


            elif side=="Sell":


                close_side="Buy"


            else:


                return None





            result=self.place_order(


                close_side,


                size,


                True


            )



            add_log(

                "POSITION CLOSE ORDER"

            )


            return result





        except Exception as e:


            add_log(

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
