# =====================================================
# portfolio/position_manager.py
# Position Management System
# =====================================================

from config import (
    DEFAULT_SYMBOL
)


from web.server import (
    update_status,
    add_log
)





class PositionManager:


    def __init__(self):


        self.position = {


            "symbol":

                DEFAULT_SYMBOL,


            "side":

                "NONE",


            "size":

                0,


            "entry":

                0,


            "mark":

                0,


            "pnl":

                0


        }



        print(

            "[POSITION MANAGER READY]"

        )









    # =====================================================
    # SYNC FROM API
    # =====================================================


    def sync(self):


        from api.bybit_api import bybit_api



        try:


            result = (

                bybit_api

                .get_position()

            )



            if not result:


                return False





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


                self.update_from_ws(

                    rows[0]

                )



            return True






        except Exception as e:


            print(

                "[POSITION SYNC ERROR]",

                e

            )


            return False









    # =====================================================
    # UPDATE FROM WS
    # =====================================================


    def update_from_ws(
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


                self.position.update({


                    "side":

                        "NONE",


                    "size":

                        0,


                    "entry":

                        0,


                    "pnl":

                        0

                })



            else:


                self.position.update({


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


                    "mark":

                        float(

                            data.get(

                                "markPrice",

                                0

                            )

                        ),


                    "pnl":

                        float(

                            data.get(

                                "unrealisedPnl",

                                0

                            )

                        )

                })








            self.dashboard_update()



            print(

                "[POSITION UPDATED]",

                self.position

            )



            return True







        except Exception as e:


            print(

                "[POSITION UPDATE ERROR]",

                e

            )


            return False









    # =====================================================
    # GET POSITION
    # =====================================================


    def get_position(self):


        return self.position









    # =====================================================
    # CHECK OPEN
    # =====================================================


    def has_position(self):


        return (

            self.position["side"]

            !=

            "NONE"

        )









    # =====================================================
    # DASHBOARD UPDATE
    # =====================================================


    def dashboard_update(self):


        update_status({


            "position":

                self.position["side"],


            "entry":

                self.position["entry"],


            "size":

                self.position["size"],


            "pnl":

                self.position["pnl"]

        })









    # =====================================================
    # RESET
    # =====================================================


    def reset(self):


        self.position = {


            "symbol":

                DEFAULT_SYMBOL,


            "side":

                "NONE",


            "size":

                0,


            "entry":

                0,


            "mark":

                0,


            "pnl":

                0

        }



        add_log(

            "POSITION RESET"

        )









# =====================================================
# INSTANCE
# =====================================================


position_manager = PositionManager()
