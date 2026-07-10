# =====================================================
# services/telegram_bot.py
# Telegram Notification Service
# =====================================================

import requests



from config import (
    TELEGRAM_ENABLED,
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID
)







class TelegramBot:



    def __init__(self):


        print(

            "[TELEGRAM INIT]",

            TELEGRAM_ENABLED

        )







    # =====================================================
    # SEND
    # =====================================================

    def send(
        self,
        message
    ):


        try:


            if not TELEGRAM_ENABLED:


                return False





            if not TELEGRAM_TOKEN:


                return False





            if not TELEGRAM_CHAT_ID:


                return False






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





            response = requests.post(

                url,

                data=data,

                timeout=5

            )



            return (

                response.status_code == 200

            )





        except Exception as e:


            print(

                "[TELEGRAM ERROR]",

                e

            )


            return False







    # =====================================================
    # BOT START
    # =====================================================

    def bot_start(self):


        self.send(

            "🚀 BYBIT BOT START"

        )







    # =====================================================
    # BOT STOP
    # =====================================================

    def bot_stop(self):


        self.send(

            "🛑 BYBIT BOT STOP"

        )







    # =====================================================
    # ERROR
    # =====================================================

    def error(
        self,
        message
    ):


        self.send(

            "❌ ERROR\n"

            +

            str(message)

        )







    # =====================================================
    # SIGNAL
    # =====================================================

    def signal(
        self,
        data
    ):


        self.send(

            "📈 SIGNAL\n"

            +

            str(data)

        )







    # =====================================================
    # ORDER
    # =====================================================

    def order(
        self,
        data
    ):


        self.send(

            "💰 ORDER\n"

            +

            str(data)

        )









# =====================================================
# SINGLETON
# =====================================================

telegram_bot = TelegramBot()
