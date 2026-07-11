# =====================================================
# api/bybit_api.py
# Bybit V5 API Manager
# =====================================================

from pybit.unified_trading import HTTP

import time



from config import (

    BYBIT_API_KEY,

    BYBIT_API_SECRET,

    CATEGORY,

    SYMBOL

)





class BybitAPI:


    def __init__(self):


        self.mode = "DEMO"


        self.session = None



        self.change_session(

            self.mode

        )



        print(

            "[BYBIT READY]",

            self.mode

        )









    # =====================================================
    # SESSION CHANGE
    # =====================================================

    def change_session(

        self,

        mode

    ):


        mode = str(mode).upper()



        self.mode = mode





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

                api_key=BYBIT_API_KEY,

                api_secret=BYBIT_API_SECRET

            )





        print(

            "[BYBIT SESSION CHANGE]",

            mode

        )









    # =====================================================
    # SAFE REQUEST
    # =====================================================

    def request(

        self,

        func,

        **kwargs

    ):


        try:


            result = func(

                **kwargs

            )



            return result





        except Exception as e:


            print(

                "[BYBIT API ERROR]",

                e

            )


            return None










    # =====================================================
    # SERVER TIME
    # =====================================================

    def server_time(self):


        return self.request(

            self.session.get_server_time

        )









    # =====================================================
    # BALANCE
    # =====================================================

    def get_balance(self):


        return self.request(

            self.session.get_wallet_balance,

            accountType="UNIFIED"

        )









    # =====================================================
    # POSITION
    # =====================================================

    def get_position(self):


        return self.request(

            self.session.get_positions,

            category=CATEGORY,

            symbol=SYMBOL

        )









    # =====================================================
    # KLINE
    # =====================================================

    def get_kline(

        self,

        interval="5",

        limit=200

    ):


        return self.request(

            self.session.get_kline,

            category=CATEGORY,

            symbol=SYMBOL,

            interval=interval,

            limit=limit

        )









    # =====================================================
    # LAST PRICE
    # =====================================================

    def get_price(self):


        result = self.request(

            self.session.get_tickers,

            category=CATEGORY,

            symbol=SYMBOL

        )



        try:


            return float(

                result["result"]["list"][0]["lastPrice"]

            )



        except:


            return 0










    # =====================================================
    # PLACE ORDER
    # =====================================================

    def place_order(

        self,

        side,

        qty

    ):


        print(

            "[ORDER]",

            self.mode,

            side,

            qty

        )



        return self.request(

            self.session.place_order,

            category=CATEGORY,

            symbol=SYMBOL,

            side=side,

            orderType="Market",

            qty=str(qty),

            timeInForce="IOC"

        )









    # =====================================================
    # CLOSE POSITION
    # =====================================================

    def close_position(

        self

    ):


        position = self.get_position()



        if not position:


            return None



        try:


            data = (

                position

                ["result"]

                ["list"]

            )[0]



            size = float(

                data.get(

                    "size",

                    0

                )

            )



            side = data.get(

                "side"

            )



            if size <= 0:


                return None





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
    # SET TP / SL
    # =====================================================

    def set_trading_stop(

        self,

        take_profit,

        stop_loss

    ):


        return self.request(

            self.session.set_trading_stop,

            category=CATEGORY,

            symbol=SYMBOL,

            takeProfit=str(

                take_profit

            ),

            stopLoss=str(

                stop_loss

            )

        )









    # =====================================================
    # LEVERAGE
    # =====================================================

    def set_leverage(

        self,

        leverage

    ):


        return self.request(

            self.session.set_leverage,

            category=CATEGORY,

            symbol=SYMBOL,

            buyLeverage=str(leverage),

            sellLeverage=str(leverage)

        )









# =====================================================
# INSTANCE
# =====================================================

bybit_api = BybitAPI()
