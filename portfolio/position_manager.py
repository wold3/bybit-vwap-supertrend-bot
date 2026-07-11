# =====================================================
# portfolio/position_manager.py
# Position Management System
# =====================================================

import threading





from api.bybit_api import bybit_api


from web.server import (
    update_status,
    add_log
)









class PositionManager:


    def __init__(self):


        self.position = {


            "side":

                "NONE",


            "size":

                0,


            "entry":

                0,


            "pnl":

                0


        }


        self.lock = threading.Lock()



        print(

            "[POSITION MANAGER READY]"

        )









    # =====================================================
    # SYNC REST
    # =====================================================

    def sync(self):


        try:


            result = (

                bybit_api

                .get_position()

            )



            if not result:


                return





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





            if rows:


                self.update_position(

                    rows[0]

                )







        except Exception as e:


            print(

                "[POSITION SYNC ERROR]",

                e

            )









    # =====================================================
    # UPDATE FROM WS
    # =====================================================

    def update_from_ws(
        self,
        data
    ):


        try:


            self.update_position(

                data

            )



        except Exception as e:


            print(

                "[WS POSITION ERROR]",

                e

            )









    # =====================================================
    # UPDATE
    # =====================================================

    def update_position(
        self,
        data
    ):


        try:


            side = data.get(

                "side",

                ""

            )



            size = float(

                data.get(

                    "size",

                    0

                )

            )



            entry = float(

                data.get(

                    "avgPrice",

                    0

                )

            )



            pnl = float(

                data.get(

                    "unrealisedPnl",

                    0

                )

            )







            if size <= 0:


                side = "NONE"









            with self.lock:


                self.position = {


                    "side":

                        side,


                    "size":

                        size,


                    "entry":

                        entry,


                    "pnl":

                        pnl


                }









            update_status({


                "position":

                    side,


                "size":

                    size,


                "entry":

                    entry,


                "pnl":

                    pnl


            })



            add_log(

                f"POSITION {side} {size}"

            )







        except Exception as e:


            print(

                "[POSITION UPDATE ERROR]",

                e

            )









    # =====================================================
    # GET
    # =====================================================

    def get_position(self):


        with self.lock:


            return self.position.copy()










    # =====================================================
    # HAS POSITION
    # =====================================================

    def has_position(self):


        with self.lock:


            return (

                self.position["size"]

                >

                0

            )









    # =====================================================
    # SIDE
    # =====================================================

    def get_side(self):


        with self.lock:


            return self.position["side"]










# =====================================================
# INSTANCE
# =====================================================

position_manager = PositionManager()
