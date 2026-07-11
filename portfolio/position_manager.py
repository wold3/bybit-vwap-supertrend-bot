# =====================================================
# portfolio/position_manager.py
# BYBIT V5 POSITION MANAGER
# =====================================================

import threading
import time


from api.bybit_api import bybit_api


from web.server import (

    add_log,

    update_status

)



class PositionManager:


    def __init__(self):

        self.lock = threading.Lock()


        self.position = {

            "symbol": "",

            "side": "NONE",

            "size": 0.0,

            "entry_price": 0.0,

            "mark_price": 0.0,

            "liq_price": 0.0,

            "pnl": 0.0,

            "updated": 0

        }


        print(
            "[POSITION MANAGER READY]"
        )



    # =====================================================
    # REFRESH REST API
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



            self.update(rows[0])


            return True



        except Exception as e:


            add_log(

                f"POSITION REFRESH ERROR {e}"

            )


            return False



    # =====================================================
    # UPDATE FROM WS / REST
    # =====================================================

    def update(self, data):


        try:

            # WS가 list로 전달하는 경우

            if isinstance(data, list):

                if not data:

                    return False

                data = data[0]



            size = float(

                data.get(

                    "size",

                    0

                ) or 0

            )



            side = data.get(

                "side",

                "NONE"

            )


            if size <= 0:

                side = "NONE"



            new_position = {


                "symbol":

                    data.get(

                        "symbol",

                        ""

                    ),


                "side":

                    side,


                "size":

                    size,


                "entry_price":

                    float(

                        data.get(

                            "avgPrice",

                            0

                        ) or 0

                    ),



                "mark_price":

                    float(

                        data.get(

                            "markPrice",

                            0

                        ) or 0

                    ),



                "liq_price":

                    float(

                        data.get(

                            "liqPrice",

                            0

                        ) or 0

                    ),



                "pnl":

                    float(

                        data.get(

                            "unrealisedPnl",

                            0

                        ) or 0

                    ),



                "updated":

                    time.time()

            }



            with self.lock:

                self.position.update(

                    new_position

                )



            update_status({

                "position":

                    new_position["side"],


                "position_size":

                    new_position["size"],


                "entry_price":

                    new_position["entry_price"],


                "pnl":

                    new_position["pnl"]

            })



            return True



        except Exception as e:


            add_log(

                f"POSITION UPDATE ERROR {e}"

            )


            return False



    # =====================================================
    # GET POSITION
    # =====================================================

    def get_position(self):


        with self.lock:

            return self.position.copy()



    # =====================================================
    # POSITION CHECK
    # =====================================================

    def has_position(self):


        with self.lock:

            return self.position["size"] > 0



    def is_long(self):


        with self.lock:

            return (

                self.position["side"] == "Buy"

                and

                self.position["size"] > 0

            )



    def is_short(self):


        with self.lock:

            return (

                self.position["side"] == "Sell"

                and

                self.position["size"] > 0

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


            self.position = {


                "symbol": "",

                "side": "NONE",

                "size": 0.0,

                "entry_price": 0.0,

                "mark_price": 0.0,

                "liq_price": 0.0,

                "pnl": 0.0,

                "updated": time.time()

            }



        update_status({

            "position":"NONE",

            "position_size":0,

            "entry_price":0,

            "pnl":0

        })


        add_log(

            "POSITION RESET"

        )



    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):


        try:


            self.reset()


            print(

                "[POSITION MANAGER CLOSED]"

            )



        except Exception as e:


            print(

                "[POSITION CLOSE ERROR]",

                e

            )




# =====================================================
# INSTANCE
# =====================================================

position_manager = PositionManager()
