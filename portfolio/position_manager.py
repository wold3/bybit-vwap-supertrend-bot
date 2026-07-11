# =====================================================
# portfolio/position_manager.py
# POSITION MANAGER
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
    # REFRESH FROM BYBIT
    # =====================================================

    def refresh(self):


        try:


            result = bybit_api.get_position()



            if not result:


                return False



            rows = result.get(

                "result",

                {}

            ).get(

                "list",

                []

            )



            if not rows:


                self.reset()

                return True




            p = rows[0]



            self.update(p)



            return True




        except Exception as e:


            add_log(

                f"POSITION REFRESH ERROR {e}"

            )


            return False





    # =====================================================
    # UPDATE POSITION
    # =====================================================

    def update(self, p):


        try:


            with self.lock:


                size = float(

                    p.get(

                        "size",

                        0

                    )

                )



                side = p.get(

                    "side"

                )



                if size <= 0:


                    side = "NONE"



                self.position.update({


                    "symbol":

                        p.get(

                            "symbol",

                            ""

                        ),



                    "side":

                        side,



                    "size":

                        size,



                    "entry_price":

                        float(

                            p.get(

                                "avgPrice",

                                0

                            )

                            or 0

                        ),



                    "mark_price":

                        float(

                            p.get(

                                "markPrice",

                                0

                            )

                            or 0

                        ),



                    "liq_price":

                        float(

                            p.get(

                                "liqPrice",

                                0

                            )

                            or 0

                        ),



                    "pnl":

                        float(

                            p.get(

                                "unrealisedPnl",

                                0

                            )

                            or 0

                        ),



                    "updated":

                        time.time()


                })



            update_status({

                "position":

                    self.position["side"],


                "position_size":

                    self.position["size"],


                "entry_price":

                    self.position["entry_price"],


                "pnl":

                    self.position["pnl"]

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
    # HAS POSITION
    # =====================================================

    def has_position(self):


        with self.lock:


            return self.position["size"] > 0





    # =====================================================
    # LONG CHECK
    # =====================================================

    def is_long(self):


        with self.lock:


            return (

                self.position["side"] == "Buy"

                and

                self.position["size"] > 0

            )





    # =====================================================
    # SHORT CHECK
    # =====================================================

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


        with self.lock:


            return self.position.copy()





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
