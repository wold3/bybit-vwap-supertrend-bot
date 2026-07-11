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

    update_status,

    add_log

)





app_instance = None





# =====================================================
# SHUTDOWN
# =====================================================

def shutdown():

    global app_instance


    print()

    print("====================")

    print("[SYSTEM SHUTDOWN]")

    print("====================")



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
# CTRL+C
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

    print("[MODE] MANUAL RUN")





    try:



        # -------------------------
        # WEB SERVER
        # -------------------------

        run_server()



        time.sleep(1)





        # -------------------------
        # BOT INIT
        # -------------------------

        app_instance = TradingApp()



        set_bot_instance(

            app_instance

        )



        print(

            "[TRADING APP READY]"

        )







        # -------------------------
        # BOT START
        # -------------------------

        app_instance.start()



        update_status({

            "bot":

                "RUNNING"

        })



        add_log(

            "BOT RUNNING"

        )





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





        # -------------------------
        # MAIN LOOP
        # -------------------------

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
