# =====================================================
# main.py
# VWAP SuperTrend Trading Bot
# =====================================================

import time
import traceback


from app import app


from database.database import (
    database
)







def main():


    print("====================")
    print("[SYSTEM START]")
    print("====================")



    try:


        app.start()



        while True:


            time.sleep(1)





    except KeyboardInterrupt:


        print()

        print(
            "[USER STOP]"
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



        print()

        print(
            "[SYSTEM SHUTDOWN]"
        )



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









if __name__ == "__main__":


    main()
