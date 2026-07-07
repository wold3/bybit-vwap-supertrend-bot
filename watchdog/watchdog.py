import time
import threading


class WatchDog:


    def __init__(self):


        self.last_private_ws = time.time()


        self.last_public_ws = time.time()


        self.running = True



        self.timeout = 30



        self.lock = threading.Lock()





    # =====================================
    # PRIVATE WS UPDATE
    # =====================================

    def update_private_ws(self):


        with self.lock:


            self.last_private_ws = time.time()





    # =====================================
    # PUBLIC WS UPDATE
    # =====================================

    def update_public_ws(self):


        with self.lock:


            self.last_public_ws = time.time()





    # =====================================
    # CHECK
    # =====================================

    def check(self):


        with self.lock:


            now = time.time()



            private_gap = (

                now

                -

                self.last_private_ws

            )


            public_gap = (

                now

                -

                self.last_public_ws

            )



        if private_gap > self.timeout:


            print(

                "⚠️ PRIVATE WS TIMEOUT",

                private_gap

            )


            self.restart_private_ws()





        if public_gap > self.timeout:


            print(

                "⚠️ PUBLIC WS TIMEOUT",

                public_gap

            )


            self.restart_public_ws()





    # =====================================
    # PRIVATE WS RESTART
    # =====================================

    def restart_private_ws(self):


        print(

            "RESTART PRIVATE WS"

        )


        # 실제 restart 연결 위치

        # private_ws.start()




    # =====================================
    # PUBLIC WS RESTART
    # =====================================

    def restart_public_ws(self):


        print(

            "RESTART PUBLIC WS"

        )


        # ws_client.start()




    # =====================================
    # LOOP
    # =====================================

    def start(self):


        print(

            "WATCHDOG START"

        )



        while self.running:


            try:


                self.check()



            except Exception as e:


                print(

                    "WATCHDOG ERROR",

                    e

                )



            time.sleep(5)





    # =====================================
    # STOP
    # =====================================

    def stop(self):


        self.running = False





watchdog = WatchDog()
