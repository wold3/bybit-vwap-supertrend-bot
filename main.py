# =======================================================
# main.py
# VWAP SuperTrend Trading Bot MAIN
# =======================================================


import time
import signal
import sys
import traceback



from app import TradingApp


from web.server import (

    run_server,

    set_bot_instance,

    add_log,

    update_status

)





# =======================================================
# GLOBAL
# =======================================================


bot = None

running = True





# =======================================================
# SIGNAL HANDLER
# =======================================================


def shutdown_handler(

    signum,

    frame

):

    global running


    print()

    print("====================")

    print("[SYSTEM SHUTDOWN]")

    print("====================")



    running = False



    try:


        if bot:


            bot.stop()



    except Exception as e:


        print(

            "[SHUTDOWN ERROR]",

            e

        )



    add_log(

        "SYSTEM SHUTDOWN"

    )


    sys.exit(0)





# =======================================================
# STARTUP
# =======================================================


def start():

    global bot



    print()

    print("====================")

    print(" VWAP SUPERTREND BOT ")

    print("====================")





    try:



        # ---------------------------------
        # WEB SERVER
        # ---------------------------------

        run_server()



        time.sleep(1)



        # ---------------------------------
        # BOT INSTANCE
        # ---------------------------------

        bot = TradingApp()



        set_bot_instance(

            bot

        )



        add_log(

            "BOT INSTANCE CREATED"

        )



        update_status({

            "bot":

                "STOPPED"

        })



        print(

            "[MAIN READY]"

        )





        # ---------------------------------
        # AUTO START
        # ---------------------------------

        bot.start()



        add_log(

            "AUTO START COMPLETE"

        )





        # ---------------------------------
        # MAIN LOOP
        # ---------------------------------

        while running:


            time.sleep(1)





    except Exception as e:



        traceback.print_exc()



        add_log(

            f"MAIN ERROR {e}"

        )



        try:


            if bot:


                bot.stop()



        except:


            pass





# =======================================================
# ENTRY
# =======================================================


if __name__ == "__main__":



    signal.signal(

        signal.SIGINT,

        shutdown_handler

    )


    signal.signal(

        signal.SIGTERM,

        shutdown_handler

    )



    start()
