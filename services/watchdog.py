# services/watchdog.py


import time
import threading



from api.bybit_api import (
    bybit_api
)


from config import (
    WATCHDOG_INTERVAL,
    MAX_API_ERROR
)



class Watchdog:



    def __init__(self):


        self.running = False


        self.thread = None


        self.last_heartbeat = time.time()


        self.api_error_count = 0


        self.system_ok = True



        print(
            "[WATCHDOG READY]"
        )





    # =====================================
    # START
    # =====================================

    def start(self):


        if self.running:

            return



        self.running = True



        self.thread = threading.Thread(

            target=self.monitor

        )


        self.thread.daemon = True


        self.thread.start()



        print(

            "[WATCHDOG START]"

        )







    # =====================================
    # LOOP
    # =====================================

    def monitor(self):


        while self.running:


            try:


                self.check_api()


                self.check_health()



            except Exception as e:


                print(

                    "[WATCHDOG ERROR]",

                    e

                )



            time.sleep(

                WATCHDOG_INTERVAL

            )









    # =====================================
    # API CHECK
    # =====================================

    def check_api(self):


        result = (

            bybit_api.ping()

        )



        if result:


            self.api_error_count = 0


            self.system_ok = True



        else:


            self.api_error_count += 1



            print(

                "[API ERROR COUNT]",

                self.api_error_count

            )



            if self.api_error_count >= MAX_API_ERROR:


                self.emergency_stop()







    # =====================================
    # HEALTH CHECK
    # =====================================

    def check_health(self):


        now = time.time()



        if (

            now - self.last_heartbeat

            >

            WATCHDOG_INTERVAL * 5

        ):


            print(

                "[WATCHDOG WARNING] NO HEARTBEAT"

            )







    # =====================================
    # HEARTBEAT
    # =====================================

    def heartbeat(self):


        self.last_heartbeat = time.time()






    # =====================================
    # EMERGENCY STOP
    # =====================================

    def emergency_stop(self):


        print(

            "==================="

        )

        print(

            "[WATCHDOG EMERGENCY STOP]"

        )

        print(

            "API FAILURE"

        )

        print(

            "==================="

        )


        self.system_ok = False






    # =====================================
    # STATUS
    # =====================================

    def status(self):


        return {


            "running":

            self.running,


            "system_ok":

            self.system_ok,


            "api_errors":

            self.api_error_count,


            "heartbeat":

            self.last_heartbeat

        }







    # =====================================
    # STOP
    # =====================================

    def stop(self):


        self.running = False



        print(

            "[WATCHDOG STOP]"

        )







watchdog = Watchdog()
