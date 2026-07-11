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
    # SYNC POSITION
    # =====================================================


    def sync(self):


        result = self.api.request(

            "GET",

            "/v5/position/list",

            {


                "category":

                    CATEGORY,


                "symbol":

                    DEFAULT_SYMBOL

            }

        )




        if not result:


            raise Exception(

                "POSITION API ERROR"

            )






        if result.get(

            "retCode"

        ) != 0:


            raise Exception(

                result.get(

                    "retMsg",

                    "POSITION ERROR"

                )

            )







        try:


            data = (

                result

                ["result"]

                ["list"]

            )



            if not data:


                self.clear()

                return self.position







            pos = data[0]



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






            return self.position





        except Exception as e:


            print(

                "[POSITION PARSE ERROR]",

                e

            )


            self.clear()


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


            "mark":

                0,


            "pnl":

                0

        }







    # =====================================================
    # GET
    # =====================================================


    def get_position(self):


        return self.position








    # =====================================================
    # HAS POSITION
    # =====================================================


    def has_position(self):


        return (

            self.position["size"]

            >

            0

        )








# =====================================================
# SINGLETON
# =====================================================


from api.bybit_api import bybit_api


position_manager = PositionManager(

    bybit_api

)
