# =====================================================
# portfolio/position_manager.py
# Position Manager
# =====================================================

import threading



from web.server import (

    update_status,

    add_log

)







class PositionManager:


    def __init__(self):


        self.lock = threading.Lock()



        self.position = {

            "side": "NONE",

            "size": 0.0,

            "entry_price": 0.0,

            "pnl": 0.0

        }



        print(

            "[POSITION MANAGER READY]"

        )









    # =====================================================
    # SAFE FLOAT
    # =====================================================

    def safe_float(

        self,

        value,

        default=0.0

    ):


        try:


            if value in [

                "",

                None

            ]:


                return default



            return float(value)



        except:


            return default









    # =====================================================
    # UPDATE FROM BYBIT WS
    # =====================================================

    def update(

        self,

        data

    ):


        try:



            with self.lock:



                if not data:


                    return






                item = data[0]





                size = self.safe_float(

                    item.get(

                        "size",

                        0

                    )

                )





                entry = self.safe_float(

                    item.get(

                        "avgPrice",

                        0

                    )

                )





                pnl = self.safe_float(

                    item.get(

                        "unrealisedPnl",

                        0

                    )

                )





                side = item.get(

                    "side",

                    ""

                )



                if size <= 0:



                    side = "NONE"





                self.position = {


                    "side":

                        side,


                    "size":

                        size,


                    "entry_price":

                        entry,


                    "pnl":

                        pnl


                }






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





        except Exception as e:



            add_log(

                f"POSITION UPDATE ERROR {e}"

            )









    # =====================================================
    # GET
    # =====================================================

    def get_position(self):


        with self.lock:


            return self.position.copy()









    # =====================================================
    # RESET
    # =====================================================

    def reset(self):


        with self.lock:



            self.position = {


                "side":

                    "NONE",


                "size":

                    0.0,


                "entry_price":

                    0.0,


                "pnl":

                    0.0


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
