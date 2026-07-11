# =====================================================
# watchdog/watchdog.py
# VWAP SUPERTREND BOT WATCHDOG
# =====================================================

import threading
import time



from web.server import (

    add_log,

    update_status

)





class Watchdog:



    def __init__(self):


        self.running = False


        self.thread = None


        self.interval = 10



        print(

            "[WATCHDOG READY]"

        )








    # =====================================================
    # START
    # =====================================================

    def start(self):


        if self.running:


            return False



        self.running = True



        self.thread = threading.Thread(

            target=self.loop,

            daemon=True,

            name="Watchdog"

        )



        self.thread.start()



        add_log(

            "WATCHDOG START"

        )



        return True







    # =====================================================
    # STOP
    # =====================================================

    def stop(self):


        self.running=False



        add_log(

            "WATCHDOG STOP"

        )









    # =====================================================
    # LOOP
    # =====================================================

    def loop(self):


        while self.running:


            try:



                self.check()



                time.sleep(

                    self.interval

                )





            except Exception as e:



                add_log(

                    f"WATCHDOG ERROR {e}"

                )



                time.sleep(10)











    # =====================================================
    # CHECK
    # =====================================================

    def check(self):


        result = {}



        # -----------------------------
        # POSITION
        # -----------------------------

        try:


            from portfolio.position_manager import position_manager



            pos = position_manager.get_position()



            result["position"] = pos.get(

                "side",

                "NONE"

            )


            result["position_size"] = pos.get(

                "size",

                0

            )



            result["position_check"] = "OK"




        except Exception as e:



            result["position_check"] = str(e)









        # -----------------------------
        # API
        # -----------------------------

        try:


            from api.bybit_api import bybit_api



            price = bybit_api.get_price()



            if price:


                result["api"] = "OK"


                result["price"] = price



            else:


                result["api"]="FAIL"




        except Exception as e:



            result["api"]=str(e)








        # -----------------------------
        # STATUS
        # -----------------------------

        result["watchdog"] = "OK"



        update_status(result)



        add_log(

            "WATCHDOG CHECK OK"

        )








# =====================================================
# INSTANCE
# =====================================================

watchdog = Watchdog()
