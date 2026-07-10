# =====================================================
# services/watchdog.py
# Bot Watchdog Service
# =====================================================

import time
import threading



from web.server import (
    add_log,
    update_status
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







    # =====================================================
    # HEARTBEAT
    # =====================================================

    def heartbeat(self):


        self.last_heartbeat = time.time()







    # =====================================================
    # LOOP
    # =====================================================

    def loop(self):


        print(

            "[WATCHDOG RUNNING]"

        )



        while self.running:



            try:



                diff = (

                    time.time()

                    -

                    self.last_heartbeat

                )






                if diff > self.timeout:



                    print(

                        "[WATCHDOG WARNING] MARKET THREAD STOP"

                    )


                    add_log(

                        "WATCHDOG MARKET TIMEOUT"

                    )



                    update_status({

                        "bot":

                            "WARNING"

                    })






                else:



                    update_status({

                        "bot":

                            "RUNNING"

                    })






            except Exception as e:



                print(

                    "[WATCHDOG ERROR]",

                    e

                )



                add_log(

                    str(e)

                )





            time.sleep(10)









    # =====================================================
    # STOP
    # =====================================================

    def stop(self):


        self.running = False



        print(

            "[WATCHDOG STOP]"

        )









# =====================================================
# SINGLETON
# =====================================================

watchdog = Watchdog()
