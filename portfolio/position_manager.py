# =====================================================
# portfolio/position_manager.py
# Position Manager
# =====================================================


from config import (
    CATEGORY,
    DEFAULT_SYMBOL
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


        self.position = None


        self.size = 0


        self.entry_price = 0


        print(

            "[POSITION MANAGER READY]"

        )









    # =====================================================
    # SYNC FROM BYBIT
    # =====================================================

    def sync(self):


        try:


            result = bybit_api.request(

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


                return False





            positions = (

                result

                .get("result", {})

                .get("list", [])

            )





            if not positions:


                self.clear()

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






            side = p.get(

                "side"

            )



            self.position = side



            self.size = size



            self.entry_price = float(

                p.get(

                    "avgPrice",

                    0

                )

            )






            update_status({

                "position":

                    side

            })



            add_log(

                f"POSITION {side} {size}"

            )



            print(

                "[POSITION]",

                side,

                size

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

    def update(
        self,
        data
    ):


        try:



            self.position = data.get(

                "side"

            )



            self.size = float(

                data.get(

                    "size",

                    0

                )

            )



            self.entry_price = float(

                data.get(

                    "entryPrice",

                    0

                )

            )





            if self.size == 0:


                self.clear()



            else:


                update_status({

                    "position":

                        self.position

                })





        except Exception as e:



            print(

                "[POSITION UPDATE ERROR]",

                e

            )








    # =====================================================
    # GET POSITION
    # =====================================================

    def get_position(self):


        return self.position







    # =====================================================
    # CHECK POSITION
    # =====================================================

    def has_position(self):


        if self.position and self.size > 0:


            return True



        return False







    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):


        self.position = None


        self.size = 0


        self.entry_price = 0





        update_status({

            "position":

                "NONE"

        })









# =====================================================
# SINGLETON
# =====================================================

position_manager = PositionManager()
