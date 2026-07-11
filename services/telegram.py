# =====================================================
# services/telegram.py
# Telegram Notification
# =====================================================

import requests


from config import (
    TELEGRAM_ENABLED,
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID
)





class Telegram:


    def __init__(self):

        print(
            "[TELEGRAM READY]"
        )







    def send(
        self,
        message
    ):


        if not TELEGRAM_ENABLED:

            return False





        try:


            url = (

                "https://api.telegram.org/bot"

                +

                TELEGRAM_TOKEN

                +

                "/sendMessage"

            )



            data = {


                "chat_id":

                    TELEGRAM_CHAT_ID,


                "text":

                    message


            }





            r = requests.post(

                url,

                json=data,

                timeout=5

            )



            return (

                r.status_code == 200

            )




        except Exception as e:


            print(

                "[TELEGRAM ERROR]",

                e

            )


            return False







telegram = Telegram()
