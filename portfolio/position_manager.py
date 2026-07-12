# =====================================================
# portfolio/position_manager.py
# BYBIT V5 POSITION MANAGER
# AUTO TRADING VERSION
# =====================================================


import threading
import time


from api.bybit_api import bybit_api


import config



from web.server import (

    add_log,

    update_status,

    get_trading_symbol

)






class PositionManager:



    def __init__(self):


        self.lock = threading.Lock()


        self.position = self.default_position()


        self.last_sync = 0


        self.sync_interval = 3



        print(

            "[POSITION MANAGER READY]"

        )







    def default_position(self):


        return {


            "symbol":config.SYMBOL,


            "side":"NONE",


            "size":0.0,


            "entry_price":0.0,


            "mark_price":0.0,


            "liq_price":0.0,


            "pnl":0.0,


            "pnl_percent":0.0,


            "roe":0.0,


            "updated":time.time()

        }







    def current_symbol(self):


        try:

            return get_trading_symbol()


        except:


            return config.SYMBOL







    # =====================================================
    # SYNC
    # =====================================================

    def refresh(self):


        try:



            if (

                time.time()

                -

                self.last_sync

                <

                self.sync_interval

            ):


                return True





            result = bybit_api.get_position()



            if not result:


                return False





            rows=result.get(

                "result",

                {}

            ).get(

                "list",

                []

            )






            symbol=self.current_symbol()





            for row in rows:



                if row.get("symbol")==symbol:


                    return self.update(row)







            return True







        except Exception as e:


            add_log(

                f"POSITION SYNC ERROR {e}"

            )


            return False










    # =====================================================
    # UPDATE
    # =====================================================

    def update(self,data):


        try:



            size=float(

                data.get(

                    "size",

                    0

                )

                or 0

            )




            side=data.get(

                "side",

                "NONE"

            )





            if size<=0:


                side="NONE"

                size=0





            entry=float(

                data.get(

                    "avgPrice",

                    0

                )

                or 0

            )



            mark=float(

                data.get(

                    "markPrice",

                    0

                )

                or 0

            )



            pnl=float(

                data.get(

                    "unrealisedPnl",

                    0

                )

                or 0

            )






            leverage=float(

                config.LEVERAGE

            )







            roe=0



            if entry>0 and size>0:


                margin=(

                    entry

                    *

                    size

                    /

                    leverage

                )


                if margin:


                    roe=(

                        pnl

                        /

                        margin

                    )*100







            pos={


                "symbol":

                    data.get(

                        "symbol",

                        self.current_symbol()

                    ),



                "side":

                    side,



                "size":

                    size,



                "entry_price":

                    entry,



                "mark_price":

                    mark,



                "liq_price":

                    float(

                        data.get(

                            "liqPrice",

                            0

                        )

                        or 0

                    ),



                "pnl":

                    pnl,



                "pnl_percent":

                    roe,



                "roe":

                    roe,



                "updated":

                    time.time()

            }







            with self.lock:


                self.position=pos





            self.last_sync=time.time()





            update_status({


                "position":side,


                "position_size":size,


                "entry_price":entry,


                "mark_price":mark,


                "pnl":pnl,


                "roe":round(roe,2),


                "last_action":"POSITION SYNC"


            })





            return True





        except Exception as e:



            add_log(

                f"POSITION UPDATE ERROR {e}"

            )


            return False







    # =====================================================
    # GET
    # =====================================================

    def get_position(self):


        with self.lock:


            return self.position.copy()







    def has_position(self):


        return self.position["size"]>0






    def is_long(self):


        return (

            self.position["side"]

            =="Buy"

            and

            self.has_position()

        )







    def is_short(self):


        return (

            self.position["side"]

            =="Sell"

            and

            self.has_position()

        )








    # =====================================================
    # RESET
    # =====================================================

    def reset(self):


        with self.lock:


            self.position=self.default_position()



        update_status({

            "position":

            "NONE",

            "position_size":

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


        self.reset()


        add_log(

            "POSITION CLOSED"

        )








# =====================================================
# INSTANCE
# =====================================================

position_manager=PositionManager()
