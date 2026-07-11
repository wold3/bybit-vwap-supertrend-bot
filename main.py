# =======================================================
# main.py
# VWAP SUPERTREND BOT MAIN RUNNER
# =======================================================

import time
import signal
import sys


from app import TradingApp


from web.server import (
    run_server,
    set_bot_instance,
    add_log
)



# =======================================================
# GLOBAL
# =======================================================

bot = None



# =======================================================
# SHUTDOWN
# =======================================================

def shutdown(signum=None, frame=None):

    print()

    print("====================")
    print("[SYSTEM SHUTDOWN]")
    print("====================")


    try:

        if bot:

            bot.stop()


    except Exception as e:

        print(
            "[STOP ERROR]",
            e
        )


    sys.exit(0)





# CTRL+C 등록

signal.signal(
    signal.SIGINT,
    shutdown
)


signal.signal(
    signal.SIGTERM,
    shutdown
)





# =======================================================
# MAIN
# =======================================================

def main():


    global bot



    print()

    print("====================")
    print("[VWAP SUPERTREND BOT]")
    print("====================")




    # WEB SERVER

    run_server()



    # BOT CREATE

    bot = TradingApp()



    set_bot_instance(

        bot

    )




    # AUTO START

    bot.start()



    add_log(

        "AUTO START COMPLETE"

    )



    print()

    print("[RUNNING]")




    # MAIN LOOP

    while True:


        time.sleep(1)








# =======================================================
# RUN
# =======================================================

if __name__ == "__main__":


    main()
