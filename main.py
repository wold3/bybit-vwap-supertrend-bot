# =====================================================
# main.py
# VWAP SUPERTREND AUTO BOT
# =====================================================

import time
import signal
import sys


from app import TradingApp


from web.server import (
    run_server,
    set_bot_instance,
    add_log
)



bot = None



def shutdown(sig=None, frame=None):

    print()

    print("====================")
    print("[SYSTEM SHUTDOWN]")
    print("====================")


    try:

        if bot:

            bot.stop()


    except Exception as e:

        print(
            "STOP ERROR",
            e
        )


    sys.exit(0)





def main():


    global bot



    print()

    print("====================")
    print("[MAIN READY]")
    print("====================")



    # WEB SERVER

    run_server()



    # BOT INSTANCE

    bot = TradingApp()



    set_bot_instance(

        bot

    )



    add_log(

        "BOT INSTANCE CREATED"

    )



    # CTRL+C 처리

    signal.signal(

        signal.SIGINT,

        shutdown

    )


    signal.signal(

        signal.SIGTERM,

        shutdown

    )



    print()

    print("====================")
    print("[AUTO START]")
    print("====================")



    bot.start()



    add_log(

        "AUTO START COMPLETE"

    )



    print()

    print("[RUNNING]")



    while True:


        time.sleep(1)






if __name__ == "__main__":


    main()
