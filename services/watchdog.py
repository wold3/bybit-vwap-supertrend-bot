# services/watchdog.py


import time
import threading


from api.bybit_api import bybit_api

from portfolio.position_manager import (
    position_manager
)


class Watchdog:


    def __init__(self):


        self.running = False


        self.thread = None


        self.last_check = 0


        self.error_count = 0


        self.max_error = 5



    # =====================================
    # START
    # =====================================

    def start(self):


        if self.running:

            return



        print(
            "[WATCHDOG START]"
        )


        self.running = True



        self.thread = threading.Thread(

            target=self.monitor,

            daemon=True

        )


        self.thread.start()



    # =====================================
    # MONITOR LOOP
    # =====================================

    def monitor(self):


        while self.running:


            try:


                self.health_check()



            except Exception as e:


                self.error_count += 1


                print(

                    "[WATCHDOG ERROR]",

                    e

                )



            time.sleep(30)




    # =====================================
    # HEALTH CHECK
    # =====================================

    def health_check(self):


        self.last_check = time.time()



        # -----------------------------
        # API CHECK
        # -----------------------------

        if not bybit_api.ping():


            self.error_count += 1


            print(

                "[WATCHDOG] API FAIL"

            )


        else:


            self.error_count = max(

                0,

                self.error_count - 1

            )



        # -----------------------------
        # POSITION CHECK
        # -----------------------------


        position = (

            position_manager.get()

        )



        if position:


            size = float(

                position.get(
                    "size",
                    0
                )

            )


            if size < 0:


                print(

                    "[WATCHDOG] INVALID POSITION"

                )




        # -----------------------------
        # ERROR LIMIT
        # -----------------------------


        if self.error_count >= self.max_error:


            self.emergency_state()




    # =====================================
    # EMERGENCY
    # =====================================

    def emergency_state(self):


        print(
            "=========================="
        )

        print(
            "[WATCHDOG EMERGENCY]"
        )

        print(
            "TRADING SHOULD STOP"
        )

        print(
            "=========================="
        )


        # 실제 구현에서는
        # risk_manager.kill_switch()
        # telegram 알림
        # position close
        # 연결 재시작


    # =====================================
    # STATUS
    # =====================================

    def status(self):


        return {


            "running":

                self.running,


            "last_check":

                self.last_check,


            "error_count":

                self.error_count


        }



    # =====================================
    # STOP
    # =====================================

    def stop(self):


        print(

            "[WATCHDOG STOP]"

        )


        self.running = False




watchdog = Watchdog()
