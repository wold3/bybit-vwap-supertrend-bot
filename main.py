# =====================================================
# main.py
# VWAP SUPERTREND AUTO BOT
# Launcher
# =====================================================

import time
import signal
import sys


from app import TradingApp


from web.server import (

    run_server,

    set_bot_instance,

    update_status,

    add_log

)



app_instance = None

shutdown_called = False



# =====================================================
# SHUTDOWN
# =====================================================

def shutdown():

    global app_instance
    global shutdown_called


    if shutdown_called:

        return


    shutdown_called = True


    print()

    print("==============================")

    print("[SYSTEM SHUTDOWN]")

    print("==============================")



    try:


        if app_instance:


            app_instance.stop()



    except Exception as e:


        print(

            "[STOP ERROR]",

            e

        )



    update_status({

        "bot":

            "STOPPED"

    })



    add_log(

        "SYSTEM STOPPED"

    )



    print(

        "[PROGRAM EXIT]"

    )



    sys.exit(0)





# =====================================================
# SIGNAL HANDLER
# =====================================================

def signal_handler(

    sig,

    frame

):


    shutdown()





signal.signal(

    signal.SIGINT,

    signal_handler

)


signal.signal(

    signal.SIGTERM,

    signal_handler

)





# =====================================================
# MAIN
# =====================================================

def main():


    global app_instance



    print()

    print("==============================")

    print(" VWAP SUPERTREND AUTO BOT ")

    print("==============================")

    print("[MODE] MANUAL CONTROL")





    try:


        # ---------------------------------
        # WEB SERVER START
        # ---------------------------------

        run_server()


        time.sleep(1)





        # ---------------------------------
        # TRADING APP INIT
        # ---------------------------------

        app_instance = TradingApp()



        set_bot_instance(

            app_instance

        )



        update_status({

            "bot":

                "STOPPED"

        })



        add_log(

            "TRADING APP READY"

        )



        print(

            "[TRADING APP READY]"

        )





        print()

        print("==============================")

        print("[SYSTEM READY]")

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

            "START / STOP : Dashboard"

        )

        print(

            "EXIT : Ctrl + C"

        )

        print()





        # ---------------------------------
        # MAIN LOOP
        # ---------------------------------

        while True:


            time.sleep(1)






    except KeyboardInterrupt:


        shutdown()





    except Exception as e:


        print(

            "[MAIN ERROR]",

            e

        )


        shutdown()





# =====================================================
# ENTRY
# =====================================================

if __name__ == "__main__":


    main()
