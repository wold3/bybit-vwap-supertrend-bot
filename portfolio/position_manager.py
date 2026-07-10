# =====================================================
# portfolio/position_manager.py
# Bybit V5 Position Manager
# =====================================================

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







    # =====================================================
    # SYNC
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





                rows = (

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





                found = None





                for p in rows:


                    size = float(

                        p.get(

                            "size",

                            0

                        )

                    )



                    if size <= 0:


                        continue






                    found = {


                        "symbol":

                            p.get(

                                "symbol",

                                DEFAULT_SYMBOL

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



                        "leverage":

                            p.get(

                                "leverage"

                            ),



                        "liq_price":

                            float(

                                p.get(

                                    "liqPrice",

                                    0

                                )

                            ),



                        "updated":

                            time.time()


                    }



                    break







                self.current = found


                self.last_sync = time.time()





                if found:


                    print(

                        "[POSITION SYNC]",

                        found

                    )


                else:


                    print(

                        "[NO POSITION]"

                    )




                return self.current





            except Exception as e:


                print(

                    "[POSITION SYNC ERROR]",

                    e

                )


                return None







    # =====================================================
    # EXISTS
    # =====================================================

    def has_position(self):


        return (


            self.current is not None


            and


            self.current.get(

                "size",

                0

            ) > 0


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
