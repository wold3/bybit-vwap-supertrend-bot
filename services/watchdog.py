# =====================================================
# services/watchdog.py
# Trading Bot Watchdog
# =====================================================

import time
import threading



from config import (
    WATCHDOG_INTERVAL,
    MAX_API_ERROR
)



class Watchdog:



    def __init__(self):


        self.running = False


        self.thread = None



        self.last_heartbeat = 0


        self.api_errors = 0


        self.lock = threading.Lock()



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



        self.last_heartbeat = time.time()



        self.thread = threading.Thread(

            target=self.run,

            daemon=True

        )



        self.thread.start()



        print(

            "[WATCHDOG START]"

        )









    # =====================================================
    # LOOP
    # =====================================================

    def run(self):


        while self.running:


            try:


                self.check()



            except Exception as e:


                print(

                    "[WATCHDOG ERROR]",

                    e

                )



            time.sleep(

                WATCHDOG_INTERVAL

            )









    # =====================================================
    # CHECK
    # =====================================================

    def check(self):


        now = time.time()



        diff = (

            now

            -

            self.last_heartbeat

        )





        if diff > (

            WATCHDOG_INTERVAL * 3

        ):


            print(

                "[WATCHDOG WARNING]"

                ,

                "NO HEARTBEAT",

                round(diff,1),

                "sec"

            )







        if self.api_errors >= MAX_API_ERROR:


            print(

                "[WATCHDOG] TOO MANY API ERRORS"

            )



            self.api_errors = 0







        print(

            "[WATCHDOG OK]",

            "heartbeat:",

            round(diff,1),

            "sec",

            "api_error:",

            self.api_errors

        )











    # =====================================================
    # HEARTBEAT
    # =====================================================

    def heartbeat(self):


        with self.lock:


            self.last_heartbeat = time.time()



            self.api_errors = 0









    # =====================================================
    # API ERROR
    # =====================================================

    def api_error(self):


        with self.lock:


            self.api_errors += 1







    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "running":

                self.running,


            "last_heartbeat":

                self.last_heartbeat,


            "api_errors":

                self.api_errors


        }









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
