# =====================================================
# main.py
# VWAP SUPERTREND BOT MAIN
# =====================================================


import threading
import time



from app import TradingApp



from web.server import (

    run_server,

    add_log

)





from watchdog.watchdog import watchdog






# =====================================================
# START WEB
# =====================================================

def start_web():


    run_server()







# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":



    print()

    print("==============================")

    print(" VWAP SUPERTREND BOT ")

    print("==============================")

    print()





    # -----------------------------
    # WEB SERVER
    # -----------------------------


    web_thread = threading.Thread(

        target=start_web,

        daemon=True

    )


    web_thread.start()





    time.sleep(2)







    # -----------------------------
    # BOT
    # -----------------------------


    bot = TradingApp()



    add_log(

        "AUTO START"

    )



    bot.start()






    # -----------------------------
    # WATCHDOG
    # -----------------------------


    watchdog.start()







    add_log(

        "AUTO START COMPLETE"

    )






    try:


        while True:


            time.sleep(1)




    except KeyboardInterrupt:



        add_log(

            "MANUAL STOP"

        )



        watchdog.stop()


        bot.stop()



        print(

            "BOT CLOSED"

        )
