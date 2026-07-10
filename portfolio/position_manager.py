# =====================================================
# portfolio/position_manager.py
# Position Manager V2
# =====================================================


import time
import threading



from config import (
    DEFAULT_SYMBOL
)


from api.bybit_api import (
    bybit_api
)







class PositionManager:



    def __init__(self):


        self.lock = threading.Lock()


        self.current = None


        self.last_sync = 0



        print(

            "[POSITION MANAGER READY]"

        )









    # =====================================================
    # SYNC FROM BYBIT
    # =====================================================

    def sync(self):


        with self.lock:


            try:



                response = (

                    bybit_api

                    .get_position()

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



                            "mark_price":

                                float(

                                    p.get(

                                        "markPrice",

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



                print(

                    "[NO POSITION]"

                )



                return None






            except Exception as e:



                print(

                    "[POSITION SYNC ERROR]",

                    e

                )


                return None










    # =====================================================
    # UPDATE FROM WS
    # =====================================================

    def update_from_ws(
        self,
        data
    ):


        try:


            with self.lock:


                if not data:


                    return





                size = float(

                    data.get(

                        "size",

                        0

                    )

                )



                if size <= 0:


                    self.current = None


                    return





                self.current = {


                    "symbol":

                        data.get(

                            "symbol",

                            DEFAULT_SYMBOL

                        ),


                    "side":

                        data.get(

                            "side"

                        ),


                    "size":

                        size,


                    "entry_price":

                        float(

                            data.get(

                                "entryPrice",

                                0

                            )

                        ),


                    "unrealized_pnl":

                        float(

                            data.get(

                                "unrealisedPnl",

                                0

                            )

                        ),


                    "updated":

                        time.time()

                }



                self.last_sync = time.time()





        except Exception as e:



            print(

                "[WS POSITION ERROR]",

                e

            )









    # =====================================================
    # HAS POSITION
    # =====================================================

    def has_position(self):


        with self.lock:


            if not self.current:


                return False



            return (

                self.current.get(

                    "size",

                    0

                )

                > 0

            )









    # =====================================================
    # SIDE
    # =====================================================

    def side(self):


        if not self.current:


            return None



        return self.current.get(

            "side"

        )









    # =====================================================
    # SIZE
    # =====================================================

    def size(self):


        if not self.current:


            return 0



        return self.current.get(

            "size",

            0

        )









    # =====================================================
    # ENTRY
    # =====================================================

    def entry_price(self):


        if not self.current:


            return 0



        return self.current.get(

            "entry_price",

            0

        )









    # =====================================================
    # PNL
    # =====================================================

    def pnl(self):


        if not self.current:


            return 0



        return self.current.get(

            "unrealized_pnl",

            0

        )









    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):


        with self.lock:


            self.current = None



            print(

                "[POSITION CLEARED]"

            )









    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "symbol":

                DEFAULT_SYMBOL,


            "position":

                self.current,


            "last_sync":

                self.last_sync


        }









# =====================================================
# SINGLETON
# =====================================================

position_manager = PositionManager()
