# =====================================================
# main.py
# VWAP SUPERTREND BOT ENTRY POINT
# Manual Run Version
# =====================================================

import time
import threading
import signal
import sys





from app import (
    app
)


from web.server import (
    run_server
)


from services.telegram import (
    telegram
)





# =====================================================
# GLOBAL
# =====================================================


running = True







# =====================================================
# WEB SERVER THREAD
# =====================================================


def start_web():


    run_server()







# =====================================================
# SHUTDOWN
# =====================================================


def shutdown(
    sig=None,
    frame=None
):


    global running



    if not running:


        return



    running = False



    print()

    print("====================")

    print("[SYSTEM STOP]")

    print("====================")





    try:


        app.stop()



        telegram.bot_stop()



    except Exception as e:


        print(

            "[SHUTDOWN ERROR]",

            e

        )





    print()

    print("[EXIT COMPLETE]")



    sys.exit(0)









# =====================================================
# SIGNAL HANDLER
# =====================================================


signal.signal(

    signal.SIGINT,

    shutdown

)


signal.signal(

    signal.SIGTERM,

    shutdown

)









# =====================================================
# MAIN
# =====================================================


def main():


    print()

    print("==============================")

    print(" VWAP SUPERTREND AUTO BOT ")

    print("==============================")





    print(

        "[MODE]",

        "MANUAL RUN"

    )









    # Telegram START


    telegram.bot_start()









    # Dashboard


    web_thread = threading.Thread(

        target=start_web,

        daemon=True

    )


    web_thread.start()









    time.sleep(2)









    # Trading System Start


    app.start()









    print()

    print("==============================")

    print("[BOT RUNNING]")

    print("==============================")

    print()

    print(

        "Dashboard:"

    )

    print(

        "http://127.0.0.1:8000"

    )

    print()

    print(

        "STOP : Ctrl + C"

    )









    while running:


        time.sleep(1)









# =====================================================
# EXECUTE
# =====================================================


if __name__ == "__main__":


    main()
