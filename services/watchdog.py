# =====================================================
# services/watchdog.py
# System Watchdog
# =====================================================

import time
import threading



from web.server import (
    update_status,
    add_log
)





class Watchdog:


    def __init__(self):


        self.running = False


        self.thread = None


        self.last_heartbeat = time.time()


        self.timeout = 60



        print(

            "[WATCHDOG READY]"

        )









    # =====================================================
    # START
    # =====================================================


    def start(self):


        if self.running:


            return



        self.running = True



        self.thread = threading.Thread(

            target=self.loop,

            daemon=True

        )


        self.thread.start()



        print(

            "[WATCHDOG RUNNING]"

        )









    # =====================================================
    # HEARTBEAT
    # =====================================================


    def heartbeat(self):


        self.last_heartbeat = time.time()







    # =====================================================
    # LOOP
    # =====================================================


    def loop(self):


        while self.running:


            try:


                delay = (

                    time.time()

                    -

                    self.last_heartbeat

                )





                if delay > self.timeout:


                    self.warning(

                        f"MARKET THREAD STOP {int(delay)} sec"

                    )



                else:


                    update_status({

                        "watchdog":

                            "OK"

                    })





            except Exception as e:


                print(

                    "[WATCHDOG ERROR]",

                    e

                )





            time.sleep(10)









    # =====================================================
    # WARNING
    # =====================================================


    def warning(
        self,
        message
    ):


        print(

            "[WATCHDOG WARNING]",

            message

        )



        add_log(

            message

        )



        update_status({

            "watchdog":

                "WARNING"

        })









    # =====================================================
    # STOP
    # =====================================================


    def stop(self):


        self.running = False



        print(

            "[WATCHDOG STOP]"

        )









# =====================================================
# INSTANCE
# =====================================================


watchdog = Watchdog()
