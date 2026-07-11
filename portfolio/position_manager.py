# =====================================================
# portfolio/position_manager.py
# VWAP SUPERTREND BOT
# BYBIT V5 POSITION MANAGER
# =====================================================

import threading
import time


from api.bybit_api import bybit_api


import config


from web.server import (

    add_log,

    update_status,

    get_trading_symbol

)





class PositionManager:



    def __init__(self):


        self.lock = threading.Lock()


        self.position = self.default_position()


        self.last_sync = 0



        print(

            "[POSITION MANAGER READY]"

        )





    # =====================================================
    # DEFAULT
    # =====================================================

    def default_position(self):


        return {


            "symbol":

                config.SYMBOL,


            "side":

                "NONE",


            "size":

                0.0,


            "entry_price":

                0.0,


            "mark_price":

                0.0,


            "liq_price":

                0.0,


            "pnl":

                0.0,


            "updated":

                time.time()

        }






    # =====================================================
    # CURRENT SYMBOL
    # =====================================================

    def current_symbol(self):


        try:

            return get_trading_symbol()


        except Exception:


            return config.SYMBOL






    # =====================================================
    # REFRESH FROM BYBIT
    # =====================================================

    def refresh(self):


        try:


            result = bybit_api.get_position()



            if not result:

                return False





            rows = []



            if isinstance(result, dict):


                rows = (

                    result

                    .get(

                        "result",

                        {}

                    )

                    .get(

                        "list",

                        []

                    )

                )



            elif isinstance(result, list):


                rows = result





            if not rows:


                self.reset()


                return True






            symbol = self.current_symbol()



            for row in rows:


                if row.get("symbol") == symbol:


                    self.update(row)


                    return True





            self.reset()


            return True





        except Exception as e:


            add_log(

                f"POSITION REFRESH ERROR {e}"

            )


            return False







    # =====================================================
    # UPDATE POSITION
    # =====================================================

    def update(self, data):


        try:



            if isinstance(data, list):


                for row in data:

                    self.update(row)


                return True





            if not isinstance(data, dict):


                return False





            symbol = data.get(

                "symbol",

                self.current_symbol()

            )



            if symbol != self.current_symbol():


                return False






            size = float(

                data.get(

                    "size",

                    0

                )

                or 0

            )





            side = data.get(

                "side",

                "NONE"

            )



            if side not in [

                "Buy",

                "Sell"

            ]:


                side = "NONE"





            if size <= 0:


                size = 0

                side = "NONE"






            position = {


                "symbol":

                    symbol,



                "side":

                    side,



                "size":

                    size,



                "entry_price":

                    float(

                        data.get(

                            "avgPrice",

                            0

                        )

                        or 0

                    ),



                "mark_price":

                    float(

                        data.get(

                            "markPrice",

                            0

                        )

                        or 0

                    ),



                "liq_price":

                    float(

                        data.get(

                            "liqPrice",

                            0

                        )

                        or 0

                    ),



                "pnl":

                    float(

                        data.get(

                            "unrealisedPnl",

                            0

                        )

                        or 0

                    ),



                "updated":

                    time.time()

            }







            with self.lock:


                self.position = position




            self.last_sync = time.time()






            update_status({



                "symbol":

                    position["symbol"],



                "position":

                    position["side"],



                "position_size":

                    position["size"],



                "entry_price":

                    position["entry_price"],



                "mark_price":

                    position["mark_price"],



                "liq_price":

                    position["liq_price"],



                "pnl":

                    position["pnl"],



                "updated":

                    position["updated"],



                "last_action":

                    "POSITION SYNC"

            })





            return True





        except Exception as e:


            add_log(

                f"POSITION UPDATE ERROR {e}"

            )


            return False







    # =====================================================
    # GET
    # =====================================================

    def get_position(self):


        with self.lock:


            return self.position.copy()







    # =====================================================
    # CHECK
    # =====================================================

    def has_position(self):


        with self.lock:


            return self.position["size"] > 0





    def is_long(self):


        with self.lock:


            return (

                self.position["side"]

                ==

                "Buy"

                and

                self.position["size"] > 0

            )





    def is_short(self):


        with self.lock:


            return (

                self.position["side"]

                ==

                "Sell"

                and

                self.position["size"] > 0

            )







    # =====================================================
    # STALE CHECK
    # =====================================================

    def is_stale(

        self,

        timeout=60

    ):


        return (

            time.time()

            -

            self.last_sync

            >

            timeout

        )







    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return self.get_position()







    # =====================================================
    # RESET
    # =====================================================

    def reset(self):


        with self.lock:


            self.position = self.default_position()





        update_status({



            "position":

                "NONE",



            "position_size":

                0,



            "entry_price":

                0,



            "mark_price":

                0,



            "liq_price":

                0,



            "pnl":

                0,



            "last_action":

                "POSITION RESET"

        })





        add_log(

            "POSITION RESET"

        )








    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):


        self.reset()



        add_log(

            "POSITION MANAGER CLOSED"

        )







# =====================================================
# INSTANCE
# =====================================================

position_manager = PositionManager()
