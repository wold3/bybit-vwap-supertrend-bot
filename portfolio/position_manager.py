# =====================================================
# portfolio/position_manager.py
# Position Manager
# =====================================================

from config import (
    CATEGORY,
    DEFAULT_SYMBOL
)





class PositionManager:


    def __init__(self, api):

        self.api = api


        self.position = {

            "side":"NONE",

            "size":0,

            "entry":0,

            "mark":0,

            "pnl":0

        }


        print(
            "[POSITION MANAGER READY]"
        )








    # =====================================================
    # REST SYNC
    # =====================================================


    def sync(self):


        result = self.api.get_position()



        if not result:

            return self.position





        if result.get("retCode") != 0:

            print(

                "[POSITION ERROR]",

                result

            )

            return self.position







        try:


            pos = result["result"]["list"][0]



            size = float(

                pos.get(

                    "size",

                    0

                )

            )



            if size == 0:


                self.clear()



            else:


                self.position = {


                    "side":

                        pos.get(

                            "side",

                            "NONE"

                        ),


                    "size":

                        size,


                    "entry":

                        float(

                            pos.get(

                                "avgPrice",

                                0

                            )

                        ),


                    "mark":

                        float(

                            pos.get(

                                "markPrice",

                                0

                            )

                        ),


                    "pnl":

                        float(

                            pos.get(

                                "unrealisedPnl",

                                0

                            )

                        )

                }





        except Exception as e:


            print(

                "[POSITION PARSE ERROR]",

                e

            )



        return self.position







    # =====================================================
    # WEBSOCKET UPDATE
    # =====================================================


    def update_ws(
        self,
        data
    ):


        try:


            if not data:

                return



            pos = data[0]



            size = float(

                pos.get(

                    "size",

                    0

                )

            )



            if size == 0:


                self.clear()


                return





            self.position = {


                "side":

                    pos.get(

                        "side",

                        "NONE"

                    ),


                "size":

                    size,


                "entry":

                    float(

                        pos.get(

                            "entryPrice",

                            0

                        )

                    ),


                "mark":

                    float(

                        pos.get(

                            "markPrice",

                            0

                        )

                    ),


                "pnl":

                    float(

                        pos.get(

                            "unrealisedPnl",

                            0

                        )

                    )

            }



            print(

                "[POSITION WS UPDATE]",

                self.position

            )





        except Exception as e:


            print(

                "[POSITION WS ERROR]",

                e

            )









    # =====================================================
    # CLEAR
    # =====================================================


    def clear(self):


        self.position = {

            "side":"NONE",

            "size":0,

            "entry":0,

            "mark":0,

            "pnl":0

        }







    def get_position(self):


        return self.position






# =====================================================
# INSTANCE
# =====================================================


from api.bybit_api import bybit_api


position_manager = PositionManager(

    bybit_api

)
