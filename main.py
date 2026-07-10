import time
import signal
import sys


from app import (
    app,
)


from utils.logger import (
    bot_logger,
)





# =====================================================
# SHUTDOWN HANDLER
# =====================================================

def shutdown(
    signum=None,
    frame=None
):


    print()


    print(
        "[MAIN SHUTDOWN]"
    )



    try:


        app.stop()



    except Exception as e:


        print(

            "[STOP ERROR]",

            e

        )





    bot_logger.info(
        "BOT STOPPED"
    )



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
# MAIN
# =====================================================

def main():



    print("====================================")
    print("VWAP SUPERTREND BOT START")
    print("====================================")




    bot_logger.info(
        "BOT START"
    )





    try:



        app.start()





        while True:



            time.sleep(1)






    except KeyboardInterrupt:


        shutdown()





    except Exception as e:


        print(

            "[MAIN ERROR]",

            e

        )


        bot_logger.exception(
            str(e)
        )


        shutdown()











if __name__ == "__main__":


    main()
