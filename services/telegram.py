# =====================================================
# services/telegram.py
# Telegram Notification Service
# =====================================================

import requests


from config import (
    TELEGRAM_ENABLE,
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID
)





class Telegram:


    def __init__(self):


        print(

            "[TELEGRAM READY]"

        )









    # =====================================================
    # SEND MESSAGE
    # =====================================================


    def send(
        self,
        message
    ):


        try:


            if not TELEGRAM_ENABLE:


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







            r = requests.post(

                url,

                data=data,

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







    # =====================================================
    # BOT START
    # =====================================================


    def bot_start(self):


        self.send(

            """

🚀 VWAP SUPERTREND BOT START

Mode:
Running

System:
ONLINE

"""

        )









    # =====================================================
    # BOT STOP
    # =====================================================


    def bot_stop(self):


        self.send(

            """

🛑 VWAP SUPERTREND BOT STOPPED

System:
OFFLINE

"""

        )









    # =====================================================
    # ORDER
    # =====================================================


    def order(
        self,
        side,
        symbol,
        qty,
        price
    ):


        self.send(

f"""
📌 ORDER EXECUTED

Symbol:
{symbol}

Side:
{side}

Qty:
{qty}

Price:
{price}

"""

        )









    # =====================================================
    # ERROR
    # =====================================================


    def error(
        self,
        error
    ):


        self.send(

f"""
⚠️ BOT ERROR

{error}

"""

        )









    # =====================================================
    # TP SL
    # =====================================================


    def tp_sl(
        self,
        tp,
        sl
    ):


        self.send(

f"""
🎯 TP / SL SET

TP:
{tp}

SL:
{sl}

"""

        )









# =====================================================
# INSTANCE
# =====================================================


telegram = Telegram()
