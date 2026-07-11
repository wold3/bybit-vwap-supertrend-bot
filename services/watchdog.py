# =====================================================
# services/watchdog.py
# Trading Bot Watchdog
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

            target=self.monitor,

            daemon=True

        )


        self.thread.start()



        update_status({

            "watchdog":

                "RUNNING"

        })









    # =====================================================
    # HEARTBEAT
    # =====================================================


    def heartbeat(self):


        self.last_heartbeat = time.time()







    # =====================================================
    # MONITOR
    # =====================================================


    def monitor(self):


        print(

            "[WATCHDOG THREAD START]"

        )



        while self.running:


            try:


                elapsed = (

                    time.time()

                    -

                    self.last_heartbeat

                )





                if elapsed > self.timeout:


                    print(

                        "[WATCHDOG WARNING]",

                        elapsed

                    )



                    add_log(

                        "WATCHDOG TIMEOUT"

                    )



                    update_status({

                        "watchdog":

                            "WARNING"

                    })





                else:


                    update_status({

                        "watchdog":

                            "HEALTHY"

                    })






            except Exception as e:


                print(

                    "[WATCHDOG ERROR]",

                    e

                )





            time.sleep(10)









    # =====================================================
    # STOP
    # =====================================================


    def stop(self):


        self.running = False



        update_status({

            "watchdog":

                "STOPPED"

        })



        print(

            "[WATCHDOG STOPPED]"

        )









# =====================================================
# INSTANCE
# =====================================================


watchdog = Watchdog()
