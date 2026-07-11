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



        self.lock = threading.Lock()



        self.last_heartbeat = time.time()


        self.timeout = 120



        self.status = "OFF"



        print(

            "[WATCHDOG READY]"

        )








    # =====================================================
    # START
    # =====================================================


    def start(self):


        with self.lock:


            if self.running:


                return



            self.running = True



        self.thread = threading.Thread(

            target=self.loop,

            daemon=True,

            name="Watchdog"

        )



        self.thread.start()



        update_status({

            "watchdog":

                "ON"

        })



        add_log(

            "WATCHDOG START"

        )









    # =====================================================
    # HEARTBEAT
    # =====================================================


    def heartbeat(self):


        with self.lock:


            self.last_heartbeat = time.time()







    # =====================================================
    # CHECK
    # =====================================================


    def check(self):


        with self.lock:


            diff = (

                time.time()

                -

                self.last_heartbeat

            )



        return diff < self.timeout







    # =====================================================
    # LOOP
    # =====================================================


    def loop(self):


        while self.running:


            try:


                alive = self.check()



                if alive:


                    self.status = "OK"



                    update_status({

                        "watchdog":

                            "OK"

                    })



                else:


                    self.status = "WARNING"



                    update_status({

                        "watchdog":

                            "WARNING"

                    })


                    add_log(

                        "WATCHDOG : NO HEARTBEAT"

                    )




            except Exception as e:


                add_log(

                    f"WATCHDOG ERROR {e}"

                )



            time.sleep(10)









    # =====================================================
    # STATUS
    # =====================================================


    def get_status(self):


        return {


            "status":

                self.status,


            "last_heartbeat":

                self.last_heartbeat,


            "timeout":

                self.timeout


        }









    # =====================================================
    # STOP
    # =====================================================


    def stop(self):


        with self.lock:


            self.running = False



        update_status({

            "watchdog":

                "OFF"

        })


        add_log(

            "WATCHDOG STOP"

        )



        print(

            "[WATCHDOG STOPPED]"

        )









# =====================================================
# INSTANCE
# =====================================================


watchdog = Watchdog()
