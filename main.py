# =====================================================
# main.py
# VWAP SUPERTREND BOT MAIN
# =====================================================

import time
import traceback
import signal
import sys



from app import (
    app
)


from database.database import (
    database
)


from web.server import (
    add_log
)





RUNNING = True





# =====================================================
# SIGNAL HANDLER
# =====================================================


def shutdown(
    signum=None,
    frame=None
):


    global RUNNING



    print(

        "\n===================="

    )


    print(

        "[SYSTEM SHUTDOWN]"

    )


    print(

        "===================="

    )



    RUNNING = False



    try:


        app.stop()



    except Exception as e:


        print(

            "[STOP ERROR]",

            e

        )



    print(

        "[PROGRAM EXIT]"

    )


    sys.exit(0)









# =====================================================
# MAIN
# =====================================================


def main():


    print(

        "===================="

    )


    print(

        "[BOT LAUNCH]"

    )


    print(

        "===================="

    )





    try:


        app.start()



        add_log(

            "BOT START COMPLETE"

        )





        while RUNNING:


            time.sleep(1)







    except KeyboardInterrupt:


        shutdown()





    except Exception as e:


        print(

            "[MAIN ERROR]",

            e

        )



        traceback.print_exc()



        try:


            database.save_error(

                e

            )


        except:


            pass



        shutdown()







# =====================================================
# REGISTER SIGNAL
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
# START
# =====================================================


if __name__ == "__main__":


    main()
