# =====================================================
# services/watchdog.py
# Bot Watchdog Service
# =====================================================

import time
import threading





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
    # HEARTBEAT
    # =====================================================


    def heartbeat(self):


        self.last_heartbeat = time.time()







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
    # LOOP
    # =====================================================


    def loop(self):


        while self.running:


            now = time.time()



            diff = (

                now -

                self.last_heartbeat

            )



            if diff > self.timeout:


                print(

                    "[WATCHDOG WARNING]"

                )


                print(

                    "NO MARKET HEARTBEAT",

                    diff

                )



                self.recovery()





            time.sleep(10)









    # =====================================================
    # RECOVERY
    # =====================================================


    def recovery(self):


        print(

            "[WATCHDOG RECOVERY]"

        )



        # 향후 추가 가능

        # websocket reconnect

        # market thread restart

        # api reconnect







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
