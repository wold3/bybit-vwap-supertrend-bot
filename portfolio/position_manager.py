# portfolio/position_manager.py


from api.bybit_api import (
    bybit_api
)



class PositionManager:


    def __init__(self):


        self.position = None




    # =====================================
    # SYNC FROM BYBIT
    # =====================================

    def sync(self):


        try:


            response = (

                bybit_api

                .get_position()

            )



            if not response:


                self.position = None

                return None





            data = (

                response

                ["result"]

                ["list"]

            )



            if not data:


                self.position = None

                return None





            pos = data[0]



            size = float(

                pos.get(

                    "size",

                    0

                )

            )



            # --------------------------------
            # NO POSITION
            # --------------------------------

            if size == 0:



                self.position = None


                print(

                    "[POSITION EMPTY]"

                )


                return None





            self.position = {


                "symbol":

                pos.get(

                    "symbol"

                ),


                "side":

                pos.get(

                    "side"

                ),


                "size":

                size,


                "entry_price":

                float(

                    pos.get(

                        "avgPrice",

                        0

                    )

                ),


                "mark_price":

                float(

                    pos.get(

                        "markPrice",

                        0

                    )

                ),


                "unrealized_pnl":

                float(

                    pos.get(

                        "unrealisedPnl",

                        0

                    )

                )

            }





            print(

                "[POSITION SYNC]",

                self.position

            )



            return self.position





        except Exception as e:


            print(

                "[POSITION SYNC ERROR]",

                e

            )


            return None






    # =====================================
    # HAS POSITION
    # =====================================

    def has_position(self):


        return (

            self.position is not None

        )





    # =====================================
    # GET
    # =====================================

    def get(self):


        return self.position





    # =====================================
    # STATUS
    # =====================================

    def status(self):


        if not self.position:


            return {


                "position":

                "NONE"

            }




        return self.position





    # =====================================
    # SIDE
    # =====================================

    def side(self):


        if not self.position:


            return None



        return self.position["side"]





    # =====================================
    # SIZE
    # =====================================

    def size(self):


        if not self.position:


            return 0



        return self.position["size"]





    # =====================================
    # ENTRY PRICE
    # =====================================

    def entry_price(self):


        if not self.position:


            return 0



        return self.position["entry_price"]





    # =====================================
    # CLEAR
    # =====================================

    def clear(self):


        self.position = None





position_manager = PositionManager()
