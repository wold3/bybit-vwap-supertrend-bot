# services/telegram_bot.py


import threading
import time
import requests


from config import (
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID
)


from risk.risk_manager import (
    risk_manager
)


from portfolio.position_manager import (
    position_manager
)


from api.bybit_api import (
    bybit_api
)



class TelegramBot:



    def __init__(self):


        self.running = False


        self.thread = None


        self.offset = None




    # =====================================
    # START
    # =====================================

    def start(self):


        if not TELEGRAM_TOKEN:

            print(
                "[TELEGRAM DISABLED]"
            )

            return



        self.running = True


        self.thread = threading.Thread(

            target=self.loop,

            daemon=True

        )


        self.thread.start()



        print(
            "[TELEGRAM START]"
        )




    # =====================================
    # SEND MESSAGE
    # =====================================

    def send(
        self,
        text
    ):


        try:


            url = (

                "https://api.telegram.org/"

                f"bot{TELEGRAM_TOKEN}/sendMessage"

            )


            requests.post(

                url,

                json={

                    "chat_id":

                    TELEGRAM_CHAT_ID,


                    "text":

                    text

                },

                timeout=5

            )


        except Exception as e:


            print(

                "[TELEGRAM ERROR]",

                e

            )




    # =====================================
    # RECEIVE LOOP
    # =====================================

    def loop(self):


        while self.running:


            try:


                url = (

                    "https://api.telegram.org/"

                    f"bot{TELEGRAM_TOKEN}/getUpdates"

                )


                params = {}


                if self.offset:

                    params["offset"] = self.offset



                result = requests.get(

                    url,

                    params=params,

                    timeout=10

                ).json()



                for item in result.get(
                    "result",
                    []
                ):


                    self.offset = (

                        item["update_id"]

                        +

                        1

                    )


                    message = (

                        item
                        .get("message", {})
                        .get("text")

                    )



                    if message:

                        self.command(

                            message

                        )



            except Exception as e:


                print(

                    "[TG LOOP ERROR]",

                    e

                )



            time.sleep(2)




    # =====================================
    # COMMAND
    # =====================================

    def command(
        self,
        cmd
    ):


        cmd = cmd.lower()



        # STATUS

        if cmd == "/status":


            self.send(

                str(

                    risk_manager.status()

                )

            )



        # POSITION

        elif cmd == "/position":


            self.send(

                str(

                    position_manager.status()

                )

            )



        # RISK

        elif cmd == "/risk":


            self.send(

                str(

                    risk_manager.status()

                )

            )



        # STOP

        elif cmd == "/stop":


            risk_manager.emergency_stop()


            self.send(

                "KILL SWITCH ON"

            )



        # START

        elif cmd == "/start":


            risk_manager.reset()


            self.send(

                "TRADING ENABLED"

            )



        # CLOSE

        elif cmd == "/close":


            position = (

                position_manager.get()

            )


            if position:


                bybit_api.close_position(

                    position["side"],

                    position["size"]

                )


                self.send(

                    "POSITION CLOSED"

                )


            else:


                self.send(

                    "NO POSITION"

                )




    # =====================================
    # STOP
    # =====================================

    def stop(self):


        self.running = False




telegram_bot = TelegramBot()
