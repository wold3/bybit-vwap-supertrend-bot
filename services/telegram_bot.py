# services/telegram_bot.py


import requests
import time


from config import (
    TELEGRAM_ENABLED,
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID
)





class TelegramBot:


    def __init__(self):


        self.enabled = TELEGRAM_ENABLED


        self.token = TELEGRAM_TOKEN


        self.chat_id = TELEGRAM_CHAT_ID



        print(

            "[TELEGRAM INIT]",

            self.enabled

        )





    # =====================================
    # SEND MESSAGE
    # =====================================

    def send(
        self,
        message
    ):


        if not self.enabled:

            return False



        if not self.token or not self.chat_id:

            return False




        try:


            url = (

                f"https://api.telegram.org/"
                f"bot{self.token}/sendMessage"

            )



            data = {


                "chat_id":

                self.chat_id,


                "text":

                message,


                "parse_mode":

                "HTML"

            }





            response = requests.post(

                url,

                data=data,

                timeout=5

            )



            return response.status_code == 200





        except Exception as e:


            print(

                "[TELEGRAM ERROR]",

                e

            )


            return False







    # =====================================
    # BOT START
    # =====================================

    def bot_start(self):


        self.send(

            """
🤖 <b>BOT START</b>

Bybit VWAP SuperTrend Bot

Status:
ONLINE
            """

        )






    # =====================================
    # ORDER
    # =====================================

    def order(
        self,
        side,
        symbol,
        price,
        qty,
        tp,
        sl
    ):


        text = f"""

📌 <b>ORDER EXECUTED</b>


Symbol:
{symbol}


Side:
{side}


Price:
{price}


Qty:
{qty}


TP:
{tp}


SL:
{sl}


Time:
{time.strftime('%Y-%m-%d %H:%M:%S')}

"""


        self.send(text)







    # =====================================
    # ERROR
    # =====================================

    def error(
        self,
        message
    ):


        self.send(

            f"""

🚨 <b>BOT ERROR</b>


{message}


Time:
{time.strftime('%Y-%m-%d %H:%M:%S')}

"""

        )







    # =====================================
    # STOP
    # =====================================

    def bot_stop(self):


        self.send(

            """
🛑 <b>BOT STOPPED</b>

System shutdown
            """

        )







telegram_bot = TelegramBot()
