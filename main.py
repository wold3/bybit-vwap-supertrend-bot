# =====================================================
# main.py
# VWAP SUPERTREND BOT MAIN
# =====================================================

import time
import signal
import threading
import traceback


from app import TradingApp


from web.server import (

    run_server,

    add_log

)





app = None

shutdown_event = threading.Event()





# =====================================================
# CTRL+C HANDLER
# =====================================================

def shutdown_handler(

    signum,

    frame

):


    print()

    print("====================")

    print("[SYSTEM SHUTDOWN]")

    print("====================")



    try:


        if app:


            app.stop()



    except Exception as e:


        print(

            "[STOP ERROR]",

            e

        )


        traceback.print_exc()



    add_log(

        "SYSTEM SHUTDOWN"

    )


    shutdown_event.set()





# =====================================================
# MAIN
# =====================================================

def main():


    global app



    print()

    print("================================")

    print(" VWAP SUPERTREND TRADING BOT ")

    print("================================")




    # CTRL+C

    signal.signal(

        signal.SIGINT,

        shutdown_handler

    )


    signal.signal(

        signal.SIGTERM,

        shutdown_handler

    )





    # ---------------------------------
    # WEB SERVER
    # ---------------------------------

    web_thread = threading.Thread(

        target=run_server,

        daemon=True,

        name="WebServer"

    )


    web_thread.start()



    time.sleep(1)





    # ---------------------------------
    # BOT START
    # ---------------------------------

    try:


        app = TradingApp()


        app.start()



        add_log(

            "AUTO START COMPLETE"

        )



        print()

        print("[RUNNING]")



    except Exception as e:


        print(

            "[START ERROR]",

            e

        )


        traceback.print_exc()


        return







    # ---------------------------------
    # MAIN WAIT LOOP
    # ---------------------------------

    try:


        while not shutdown_event.is_set():


            time.sleep(1)



    except KeyboardInterrupt:


        shutdown_handler(

            None,

            None

        )





    print()

    print("[EXIT COMPLETE]")







# =====================================================
# START
# =====================================================

if __name__ == "__main__":


    main()
