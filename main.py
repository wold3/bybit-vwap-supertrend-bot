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

    update_status,

    reset_status

)



# =======================================================
# GLOBAL
# =======================================================

bot = None

running = True





# =======================================================
# SHUTDOWN HANDLER
# =======================================================

def shutdown_handler(signum, frame):

    global running
    global bot


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

            "[BOT STOP ERROR]",

            e

        )



    add_log(

        "SYSTEM SHUTDOWN COMPLETE"

    )


    time.sleep(1)


    sys.exit(0)







# =======================================================
# BOT START
# =======================================================

def start():

    global bot


    print()

    print("==============================")

    print(" VWAP SUPERTREND AUTO BOT ")

    print("==============================")



    try:


        # ---------------------------------
        # RESET STATUS
        # ---------------------------------

        reset_status()



        # ---------------------------------
        # WEB SERVER
        # ---------------------------------

        run_server()



        time.sleep(2)



        add_log(

            "WEB SERVER READY"

        )





        # ---------------------------------
        # CREATE BOT
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
        # MAIN PROCESS LOOP
        # ---------------------------------

        while running:


            time.sleep(1)





    except KeyboardInterrupt:


        shutdown_handler(

            None,

            None

        )





    except Exception as e:


        traceback.print_exc()



        add_log(

            f"MAIN FATAL ERROR {e}"

        )



        try:


            if bot:


                bot.stop()



        except Exception:


            pass





        time.sleep(5)



        # 재시작 대기

        if running:


            add_log(

                "MAIN RESTART"

            )


            start()








# =======================================================
# ENTRY POINT
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
