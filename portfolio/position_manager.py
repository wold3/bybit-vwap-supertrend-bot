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


            "side": "NONE",

            "size": 0,

            "entry": 0,

            "pnl": 0

        }


        self.lock = threading.Lock()



        print(
            "[POSITION MANAGER READY]"
        )









    # =====================================================
    # SAFE FLOAT
    # =====================================================

    def safe_float(
        self,
        value
    ):


        try:


            if value in (

                "",

                None

            ):


                return 0



            return float(value)





        except Exception:


            return 0










    # =====================================================
    # REST SYNC
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
    # UPDATE FROM WEBSOCKET
    # =====================================================

    def update_from_ws(
        self,
        data
    ):


        try:


            if isinstance(

                data,

                list

            ):


                if len(data) == 0:


                    return


                data = data[0]





            self.update_position(

                data

            )





        except Exception as e:


            print(

                "[WS POSITION ERROR]",

                e

            )









    # =====================================================
    # UPDATE POSITION
    # =====================================================

    def update_position(
        self,
        data
    ):


        try:


            if not data:


                return





            side = data.get(

                "side",

                ""

            )



            size = self.safe_float(

                data.get(

                    "size"

                )

            )



            entry = self.safe_float(

                data.get(

                    "avgPrice"

                )

            )



            pnl = self.safe_float(

                data.get(

                    "unrealisedPnl"

                )

            )





            if size <= 0:


                side = "NONE"

                size = 0

                entry = 0

                pnl = 0







            position = {


                "side":

                    side,


                "size":

                    size,


                "entry":

                    entry,


                "pnl":

                    pnl


            }








            with self.lock:


                self.position = position.copy()







            update_status({


                "position":

                    side,


                "position_size":

                    size,


                "entry_price":

                    entry,


                "pnl":

                    pnl


            })





            add_log(

                f"POSITION {side} SIZE {size}"

            )







        except Exception as e:


            print(

                "[POSITION UPDATE ERROR]",

                e

            )









    # =====================================================
    # GET POSITION
    # =====================================================

    def get_position(self):


        with self.lock:


            return self.position.copy()










    # =====================================================
    # CHECK POSITION
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


            return (

                self.position["side"]

            )









    # =====================================================
    # SIZE
    # =====================================================

    def get_size(self):


        with self.lock:


            return (

                self.position["size"]

            )









    # =====================================================
    # RESET
    # =====================================================

    def reset(self):


        with self.lock:


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









# =====================================================
# INSTANCE
# =====================================================

position_manager = PositionManager()
