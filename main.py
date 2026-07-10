# =====================================================
# main.py
# BYBIT VWAP SUPERTREND BOT
# =====================================================


import time
import traceback



from app import (
    TradingApp
)



from database.database import (
    database
)







def main():



    app = TradingApp()



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

                str(e)

            )


        except:


            pass



        try:


            app.stop()


        except:


            pass







    finally:



        try:


            database.close()


        except:


            pass







if __name__ == "__main__":



    main()
