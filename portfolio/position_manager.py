# =====================================================
# portfolio/position_manager.py
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


        self.lock = threading.RLock()


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


                    print(

                        "[POSITION SYNC EMPTY]"

                    )

                    return self.current





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




                found = False



                for p in positions:



                    size = float(

                        p.get(

                            "size",

                            0

                        )

                        or 0

                    )



                    if size <= 0:

                        continue



                    found = True



                    self.current = {



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

                                or 0

                            ),



                        "unrealized_pnl":

                            float(

                                p.get(

                                    "unrealisedPnl",

                                    0

                                )

                                or 0

                            ),



                        "updated":

                            time.time()

                    }



                    break





                if not found:


                    self.current = None





                self.last_sync = time.time()



                if self.current:


                    print(

                        "[POSITION SYNC]",

                        self.current

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


                # API 오류시 기존 데이터 유지

                return self.current





    # =====================================================
    # UPDATE FROM WS
    # =====================================================

    def update_ws(
        self,
        data
    ):


        with self.lock:


            try:


                item = data[0]


                size = float(

                    item.get(

                        "size",

                        0

                    )

                )



                if size <= 0:


                    self.current = None


                    return





                self.current = {


                    "symbol":

                        item.get(

                            "symbol"

                        ),


                    "side":

                        item.get(

                            "side"

                        ),


                    "size":

                        size,


                    "entry_price":

                        float(

                            item.get(

                                "avgPrice",

                                0

                            )

                        ),


                    "unrealized_pnl":

                        float(

                            item.get(

                                "unrealisedPnl",

                                0

                            )

                        ),


                    "updated":

                        time.time()

                }



            except Exception as e:


                print(

                    "[WS POSITION ERROR]",

                    e

                )





    # =====================================================
    # CHECK
    # =====================================================

    def has_position(self):


        with self.lock:


            return (

                self.current is not None

                and

                self.current.get(

                    "size",

                    0

                ) > 0

            )





    def is_long(self):


        return self.side() == "Buy"





    def is_short(self):


        return self.side() == "Sell"





    # =====================================================
    # GETTERS
    # =====================================================

    def side(self):


        if not self.current:

            return None


        return self.current.get(

            "side"

        )





    def size(self):


        if not self.current:

            return 0


        return self.current.get(

            "size",

            0

        )





    def entry_price(self):


        if not self.current:

            return 0


        return self.current.get(

            "entry_price",

            0

        )





    def pnl(self):


        if not self.current:

            return 0


        return self.current.get(

            "unrealized_pnl",

            0

        )





    # =====================================================
    # SNAPSHOT
    # =====================================================

    def snapshot(self):


        with self.lock:


            return self.current.copy() if self.current else None





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

                self.snapshot(),


            "last_sync":

                self.last_sync

        }





position_manager = PositionManager()
