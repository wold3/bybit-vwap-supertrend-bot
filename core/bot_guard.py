import threading
import time



class BotGuard:


    def __init__(self):

        self.running = True

        self.lock = threading.Lock()



    def stop(self):

        with self.lock:

            self.running = False



        print(
            "[GUARD STOP]"
        )




    def is_running(self):

        with self.lock:

            return self.running





    def heartbeat(self):

        print(
            "[HEARTBEAT]",
            time.strftime("%Y-%m-%d %H:%M:%S")
        )






bot_guard = BotGuard()
