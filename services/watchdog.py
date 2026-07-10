# services/watchdog.py


import time
import threading



from config import (
    WATCHDOG_INTERVAL,
    MAX_API_ERROR,
)



from api.bybit_api import (
    bybit_api
)



from risk.risk_manager import (
    risk_manager
)



from services.private_ws import (
    private_ws
)




try:

    from services.telegram_bot import (
        telegram_bot
    )

except:


    telegram_bot = None






class Watchdog:



    def __init__(self):


        self.running = False


        self.thread = None


        self.api_errors = 0


        self.last_check = 0






    # =====================================
    # START
    # =====================================

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

            "[WATCHDOG START]"

        )







    # =====================================
    # LOOP
    # =====================================

    def loop(self):


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







    # =====================================
    # HEALTH CHECK
    # =====================================

    def check(self):


        print(

            "[WATCHDOG CHECK]"

        )



        # -----------------------------
        # API CHECK
        # -----------------------------


        if not bybit_api.ping():



            self.api_errors += 1



            print(

                "[API FAILURE]",

                self.api_errors

            )



        else:



            self.api_errors = 0






        # -----------------------------
        # API FAILURE LIMIT
        # -----------------------------


        if self.api_errors >= MAX_API_ERROR:



            self.emergency_stop()



            return







        # -----------------------------
        # WS CHECK
        # -----------------------------


        ws_delay = (

            private_ws.heartbeat()

        )



        if ws_delay > 120:



            print(

                "[WS DELAY]",

                ws_delay

            )



            self.notify(

                "PRIVATE WS DELAY"

            )








        self.last_check = time.time()







    # =====================================
    # EMERGENCY
    # =====================================

    def emergency_stop(self):


        print(

            "[WATCHDOG KILL SWITCH]"

        )



        try:



            risk_manager.emergency_stop()



        except Exception:



            pass



        self.notify(

            "BOT STOPPED BY WATCHDOG"

        )







    # =====================================
    # TELEGRAM
    # =====================================

    def notify(
        self,
        message
    ):


        try:


            if telegram_bot:


                telegram_bot.send(

                    message

                )


        except Exception:


            pass






    # =====================================
    # STOP
    # =====================================

    def stop(self):


        print(

            "[WATCHDOG STOP]"

        )


        self.running = False






watchdog = Watchdog()
