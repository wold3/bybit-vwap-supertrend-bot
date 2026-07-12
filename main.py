# =====================================================
# main.py
# VWAP SUPERTREND BOT V3
# MAIN EXECUTOR
# =====================================================


import threading

import time

import signal

import sys





from app import TradingApp


from web.server import (

    run_server,

    add_log

)








# =====================================================
# GLOBAL
# =====================================================


bot = None



server_thread = None







# =====================================================
# START
# =====================================================


def start():

    global bot


    add_log(

        "SYSTEM START"

    )





    # BOT INSTANCE


    bot = TradingApp()






    # WEB SERVER


    global server_thread



    server_thread = threading.Thread(

        target=run_server,

        daemon=True

    )



    server_thread.start()



    time.sleep(2)





    add_log(

        "WEB SERVER START :8000"

    )







    # AUTO START OPTION


    # 자동매매 바로 시작하려면 True

    AUTO_START = True



    if AUTO_START:


        bot.start()






    add_log(

        "SYSTEM READY"

    )









# =====================================================
# STOP
# =====================================================


def shutdown(

    signum=None,

    frame=None

):


    add_log(

        "SYSTEM SHUTDOWN"

    )



    try:


        if bot:


            bot.stop()



    except Exception as e:


        add_log(

            f"STOP ERROR {e}"

        )



    time.sleep(1)



    sys.exit(0)









# =====================================================
# SIGNAL
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
# RUN
# =====================================================


if __name__ == "__main__":


    start()



    try:



        while True:


            time.sleep(1)




    except KeyboardInterrupt:


        shutdown()
