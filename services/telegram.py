# =====================================================
# services/telegram.py
# Telegram Notification Service
# =====================================================

import requests


from config import (
    TELEGRAM_ENABLED,
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID
)





class Telegram:


    def __init__(self):


        if TELEGRAM_ENABLED:

            print(
                "[TELEGRAM READY]"
            )

        else:

            print(
                "[TELEGRAM DISABLED]"
            )







    # =====================================================
    # SEND MESSAGE
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





            r = requests.post(

                url,

                json=data,

                timeout=10

            )





            if r.status_code == 200:


                print(

                    "[TELEGRAM SENT]"

                )


                return True



            else:


                print(

                    "[TELEGRAM ERROR]",

                    r.text

                )



                return False





        except Exception as e:


            print(

                "[TELEGRAM ERROR]",

                e

            )


            return False







    # =====================================================
    # START
    # =====================================================


    def bot_start(self):


        self.send(

"""
🟢 VWAP SUPERTREND BOT START

System Online

Market Scanner Running
"""

        )







    # =====================================================
    # STOP
    # =====================================================


    def bot_stop(self):


        self.send(

"""
🔴 VWAP SUPERTREND BOT STOP

System Shutdown
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
🚀 ORDER EXECUTED

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
# INSTANCE
# =====================================================


telegram = Telegram()
