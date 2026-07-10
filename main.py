# =====================================================
# main.py
# Trading Bot Entry Point
# =====================================================


import time
import traceback



from app import (
    app
)


from database.database import (
    database
)







def main():


    try:



        app.start()



        while True:



            time.sleep(1)







    except KeyboardInterrupt:



        print()

        print(

            "[USER STOP]"

        )



        app.stop()







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



        app.stop()







    finally:



        print(

            "[PROGRAM EXIT]"

        )









if __name__ == "__main__":


    main()
