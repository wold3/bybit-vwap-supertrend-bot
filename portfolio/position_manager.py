# portfolio/position_manager.py


import time
import threading



from api.bybit_api import (
    bybit_api
)


from config import (
    DEFAULT_SYMBOL
)





class PositionManager:



    def __init__(self):


        self.lock = threading.Lock()


        self.current = None


        self.last_sync = 0



        print(

            "[POSITION MANAGER READY]"

        )






    # =====================================
    # SYNC POSITION
    # =====================================

    def sync(self):


        with self.lock:


            try:


                response = (

                    bybit_api.get_position()

                )



                if not response:


                    self.current = None

                    return None





                positions = (

                    response

                    .get(

                        "result",

                        {}

                    )

                    .get(

                        "list",

                        []

                    )

                )





                for p in positions:



                    size = float(

                        p.get(

                            "size",

                            0

                        )

                    )



                    if size > 0:



                        self.current = {


                            "symbol":

                            p.get(

                                "symbol"

                            ),



                            "side":

                            p.get(

                                "side"

                            ),



                            "size":

                            size,



                            "entry_price":

                            float(

                                p.get(

                                    "avgPrice",

                                    0

                                )

                            ),



                            "unrealized_pnl":

                            float(

                                p.get(

                                    "unrealisedPnl",

                                    0

                                )

                            ),



                            "updated":

                            time.time()

                        }




                        self.last_sync = time.time()



                        print(

                            "[POSITION SYNC]",

                            self.current

                        )



                        return self.current






                self.current = None


                self.last_sync = time.time()



                return None






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


        if self.current:


            if self.current.get(

                "size",

                0

            ) > 0:


                return True



        return False







    # =====================================
    # SIDE
    # =====================================

    def side(self):


        if not self.current:


            return None



        return self.current.get(

            "side"

        )







    # =====================================
    # SIZE
    # =====================================

    def size(self):


        if not self.current:


            return 0



        return self.current.get(

            "size",

            0

        )








    # =====================================
    # ENTRY PRICE
    # =====================================

    def entry_price(self):


        if not self.current:


            return 0



        return self.current.get(

            "entry_price",

            0

        )








    # =====================================
    # PNL
    # =====================================

    def pnl(self):


        if not self.current:


            return 0



        return self.current.get(

            "unrealized_pnl",

            0

        )







    # =====================================
    # CLEAR
    # =====================================

    def clear(self):


        with self.lock:


            self.current = None



            print(

                "[POSITION CLEARED]"

            )







    # =====================================
    # STATUS
    # =====================================

    def status(self):


        return {


            "symbol":

            DEFAULT_SYMBOL,


            "position":

            self.current,


            "last_sync":

            self.last_sync

        }








position_manager = PositionManager()
