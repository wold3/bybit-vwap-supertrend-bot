# =====================================================
# portfolio/position_manager.py
# Position Manager
# =====================================================

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

                0,


            "liq":

                0

        }



        print(

            "[POSITION MANAGER READY]"

        )









    # =====================================================
    # SYNC FROM API
    # =====================================================


    def sync(self):


        try:


            data = (

                bybit_api

                .get_position()

            )



            if not data:


                return False





            if data.get(

                "retCode"

            ) != 0:


                print(

                    "[POSITION API ERROR]",

                    data

                )


                return False







            items = (

                data

                ["result"]

                ["list"]

            )



            if not items:


                self.clear()


                return True






            pos = items[0]



            self.update(

                pos

            )



            return True






        except Exception as e:


            print(

                "[POSITION SYNC ERROR]",

                e

            )


            return False







    # =====================================================
    # UPDATE
    # =====================================================


    def update(
        self,
        data
    ):


        try:



            size = float(

                data.get(

                    "size",

                    0

                )

            )



            side = data.get(

                "side",

                ""

            )



            if size == 0:


                self.clear()



                return







            self.position = {


                "side":

                    side,


                "size":

                    size,


                "entry":

                    float(

                        data.get(

                            "avgPrice",

                            0

                        )

                    ),


                "pnl":

                    float(

                        data.get(

                            "unrealisedPnl",

                            0

                        )

                    ),


                "liq":

                    float(

                        data.get(

                            "liqPrice",

                            0

                        )

                    )

            }







            update_status({


                "position":

                    side,


                "size":

                    size,


                "entry":

                    self.position["entry"],


                "pnl":

                    self.position["pnl"]

            })







        except Exception as e:


            print(

                "[POSITION UPDATE ERROR]",

                e

            )









    # =====================================================
    # UPDATE FROM PRIVATE WS
    # =====================================================


    def update_from_ws(
        self,
        data
    ):


        self.update(

            data

        )



        add_log(

            "POSITION UPDATED"

        )









    # =====================================================
    # CLEAR
    # =====================================================


    def clear(self):


        self.position = {


            "side":

                "NONE",


            "size":

                0,


            "entry":

                0,


            "pnl":

                0,


            "liq":

                0

        }



        update_status({


            "position":

                "NONE",


            "size":

                0,


            "entry":

                0,


            "pnl":

                0

        })









    # =====================================================
    # GET
    # =====================================================


    def get_position(self):


        return self.position










# =====================================================
# INSTANCE
# =====================================================


position_manager = PositionManager()
