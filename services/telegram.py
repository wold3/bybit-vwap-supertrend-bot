# =====================================================
# services/telegram.py
# Telegram Notification Service
# =====================================================

import requests





from config import (

    TELEGRAM_TOKEN,

    TELEGRAM_CHAT_ID

)







class Telegram:



    def __init__(self):


        self.enabled = False



        if (

            TELEGRAM_TOKEN

            and

            TELEGRAM_CHAT_ID

        ):


            self.enabled = True



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


        if not self.enabled:


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





            response = requests.post(

                url,

                json=data,

                timeout=10

            )





            return (

                response.status_code

                ==

                200

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

🚀 BOT START

VWAP SUPERTREND BOT

Status : RUNNING

"""

        )









    # =====================================================
    # BOT STOP
    # =====================================================

    def bot_stop(self):


        self.send(

            """

🛑 BOT STOP

VWAP SUPERTREND BOT

Status : STOPPED

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


Side : {side}

Symbol : {symbol}

Qty : {qty}

Price : {price}

"""

        )









    # =====================================================
    # POSITION
    # =====================================================

    def position(

        self,

        side,

        size,

        pnl

    ):


        self.send(

            f"""

📊 POSITION UPDATE


Side : {side}

Size : {size}

PNL : {pnl}

"""

        )









    # =====================================================
    # ERROR
    # =====================================================

    def error(

        self,

        message

    ):


        self.send(

            f"""

⚠️ BOT ERROR


{message}

"""

        )









# =====================================================
# INSTANCE
# =====================================================

telegram = Telegram()
