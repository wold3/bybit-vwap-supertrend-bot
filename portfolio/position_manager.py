# =====================================================
# portfolio/position_manager.py
# Position Manager
# =====================================================

from config import (
    DEFAULT_SYMBOL,
    CATEGORY
)



from api.bybit_api import (
    bybit_api
)



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



        print(

            "[POSITION MANAGER READY]"

        )







    # =====================================================
    # SYNC POSITION
    # =====================================================


    def sync(self):


        try:


            result = (

                bybit_api

                .get_position()

            )



            if not result:


                return False





            if result.get(

                "retCode"

            ) != 0:


                print(

                    "[POSITION ERROR]",

                    result

                )


                return False







            positions = (

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



            if not positions:


                self.clear()



                print(

                    "[NO POSITION]"

                )


                return True







            p = positions[0]





            size = float(

                p.get(

                    "size",

                    0

                )

            )





            if size == 0:


                self.clear()



                print(

                    "[NO POSITION]"

                )


                return True







            self.position = {


                "side":

                    p.get(

                        "side",

                        "NONE"

                    ),


                "size":

                    size,


                "entry":

                    float(

                        p.get(

                            "avgPrice",

                            0

                        )

                    ),


                "pnl":

                    float(

                        p.get(

                            "unrealisedPnl",

                            0

                        )

                    )

            }





            self.update_dashboard()



            print(

                "[POSITION SYNC]",

                self.position

            )



            add_log(

                str(

                    self.position

                )

            )



            return True





        except Exception as e:


            print(

                "[POSITION SYNC ERROR]",

                e

            )


            return False







    # =====================================================
    # GET POSITION
    # =====================================================


    def get_position(self):


        return self.position







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

                0

        }



        self.update_dashboard()







    # =====================================================
    # UPDATE FROM WS
    # =====================================================


    def update_from_ws(
        self,
        data
    ):


        try:


            self.position = {


                "side":

                    data.get(

                        "side",

                        "NONE"

                    ),


                "size":

                    float(

                        data.get(

                            "size",

                            0

                        )

                    ),


                "entry":

                    float(

                        data.get(

                            "entryPrice",

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

            }



            self.update_dashboard()



        except Exception as e:


            print(

                "[WS POSITION ERROR]",

                e

            )









    # =====================================================
    # DASHBOARD
    # =====================================================


    def update_dashboard(self):


        update_status({


            "position":

                self.position["side"],


            "size":

                self.position["size"],


            "entry":

                self.position["entry"],


            "pnl":

                self.position["pnl"]

        })









# =====================================================
# INSTANCE
# =====================================================


position_manager = PositionManager()
