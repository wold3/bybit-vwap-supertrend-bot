# =====================================================
# portfolio/position_manager.py
# VWAP SUPERTREND BOT
# BYBIT V5 POSITION MANAGER
# =====================================================

import threading
import time


from api.bybit_api import bybit_api


from config import SYMBOL


from web.server import (

    add_log,

    update_status

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

            "symbol": SYMBOL,

            "side": "NONE",

            "size": 0.0,

            "entry_price": 0.0,

            "mark_price": 0.0,

            "liq_price": 0.0,

            "pnl": 0.0,

            "updated": time.time()

        }







    # =====================================================
    # REST SYNC
    # =====================================================

    def refresh(self):


        try:


            result = bybit_api.get_position()



            if not result:


                return False




            rows = (

                result

                .get("result", {})

                .get("list", [])

            )



            if not rows:


                self.reset()

                return True






            for row in rows:


                if row.get("symbol") == SYMBOL:


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
    # UPDATE
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

                SYMBOL

            )



            if symbol != SYMBOL:


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





            if size <= 0:


                side = "NONE"







            new = {


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


                old_pnl = self.position.get(

                    "pnl",

                    0

                )


                self.position = new



            self.last_sync=time.time()






            update_status({


                "position":

                    new["side"],



                "position_size":

                    new["size"],



                "entry_price":

                    new["entry_price"],



                "pnl":

                    new["pnl"]


            })







            # PNL change log

            if old_pnl != new["pnl"]:


                pass





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

                self.position["size"]

                > 0

            )






    def is_short(self):


        with self.lock:


            return (

                self.position["side"]

                ==

                "Sell"

                and

                self.position["size"]

                > 0

            )








    # =====================================================
    # WAIT SYNC
    # =====================================================

    def is_stale(self, timeout=60):


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


            "pnl":

                0


        })



        add_log(

            "POSITION RESET"

        )







    # =====================================================
    # CLOSE LOCAL STATE
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
