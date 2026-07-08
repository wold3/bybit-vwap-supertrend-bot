# watchdog/watchdog.py

import time
import threading



class Watchdog:
    """
    System Watchdog

    기능:
    - 서비스 heartbeat 기록
    - 서비스 생존 확인
    - 상태 조회
    """



    def __init__(self):


        self.running = False


        self.lock = threading.RLock()


        self.services = {}



    # =====================================
    # START
    # =====================================

    def start(self):


        with self.lock:


            self.running = True



        print(

            "[WATCHDOG START]"

        )


        return True





    # =====================================
    # STOP
    # =====================================

    def stop(self):


        with self.lock:


            self.running = False



        print(

            "[WATCHDOG STOP]"

        )


        return True





    # =====================================
    # HEARTBEAT
    # =====================================

    def heartbeat(
        self,
        service="default"
    ):


        with self.lock:


            self.services[service] = {


                "time":

                    time.time(),


                "alive":

                    True

            }



        return True





    # =====================================
    # CHECK SERVICE
    # =====================================

    def is_alive(
        self,
        service,
        timeout=60
    ):


        with self.lock:


            data = self.services.get(

                service

            )



            if not data:


                return False



            return (

                time.time()

                -

                data["time"]

            ) <= timeout





    # =====================================
    # ALL STATUS
    # =====================================

    def status(self):


        with self.lock:


            now = time.time()


            result = {}



            for name, data in self.services.items():


                result[name] = {


                    "alive":

                        (

                            now

                            -

                            data["time"]

                        )

                        <= 60,


                    "last":

                        data["time"]

                }



            return {


                "running":

                    self.running,


                "services":

                    result

            }





    # =====================================
    # RESET
    # =====================================

    def reset(self):


        with self.lock:


            self.services.clear()


            self.running = False





watchdog = Watchdog()
