# =====================================================
# services/watchdog.py
# Bot Watchdog Service
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



        update_status({

            "watchdog":

                "ON"

        })



        print(

            "[WATCHDOG START]"

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


                diff = (

                    time.time()

                    -

                    self.last_heartbeat

                )





                if diff > self.timeout:


                    update_status({


                        "watchdog":

                            "WARNING"


                    })



                    add_log(

                        "WATCHDOG WARNING : NO HEARTBEAT"

                    )





                else:


                    update_status({


                        "watchdog":

                            "OK"


                    })







                time.sleep(10)







            except Exception as e:


                print(

                    "[WATCHDOG ERROR]",

                    e

                )



            time.sleep(1)









    # =====================================================
    # STOP
    # =====================================================

    def stop(self):


        self.running = False



        update_status({


            "watchdog":

                "OFF"


        })



        print(

            "[WATCHDOG STOPPED]"

        )









# =====================================================
# INSTANCE
# =====================================================

watchdog = Watchdog()
