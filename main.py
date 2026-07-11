# =====================================================
# main.py
# VWAP SUPERTREND BOT MAIN
# =====================================================

import time
import traceback


from app import (
    app
)


from database.database import (
    database
)


from web.server import (
    add_log
)


from services.telegram import (
    telegram
)





def main():


    print("====================")
    print("[SYSTEM START]")
    print("====================")



    try:


        add_log(

            "SYSTEM START"

        )


        telegram.bot_start()



        app.start()





        while True:


            time.sleep(1)






    except KeyboardInterrupt:


        print(

            "[USER STOP]"

        )


        add_log(

            "USER STOP"

        )





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






    finally:


        print(

            "[SYSTEM SHUTDOWN]"

        )



        try:


            telegram.bot_stop()



        except:


            pass





        try:


            app.stop()



        except:


            pass






        print(

            "[PROGRAM EXIT]"

        )









if __name__ == "__main__":


    main()
