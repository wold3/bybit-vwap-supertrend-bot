# =====================================================
# api/bybit_api.py
# VWAP SUPERTREND BOT
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
    # SESSION CREATE
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


        if get_trading_mode() != self.current_mode:


            self.create_session()











    # =====================================================
    # SYMBOL
    # =====================================================

    def change_symbol(self, symbol):


        self.symbol = symbol.upper()



        add_log(

            f"SYMBOL CHANGE {self.symbol}"

        )


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



            result = self.session.get_tickers(


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


            return None












    # =====================================================
    # LEVERAGE
    # =====================================================

    def set_leverage(self):


        try:


            self.check_session()



            result = self.session.set_leverage(


                category=CATEGORY,


                symbol=self.symbol,


                buyLeverage=str(LEVERAGE),


                sellLeverage=str(LEVERAGE)


            )



            return result






        except Exception as e:



            error=str(e)



            # 이미 같은 레버리지 설정됨

            if "110043" in error or "leverage not modified" in error:


                add_log(

                    f"LEVERAGE ALREADY {LEVERAGE}X"

                )


                return True





            add_log(

                f"LEVERAGE ERROR {error}"

            )


            return None
