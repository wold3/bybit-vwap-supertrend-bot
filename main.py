# =====================================================
# main.py
# =====================================================


import time
import traceback



from app import (
    TradingApp
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
            "[KEYBOARD STOP]"
        )



        app.stop()





    except Exception as e:



        print(

            "[MAIN ERROR]",

            e

        )


        traceback.print_exc()



        app.stop()







if __name__ == "__main__":


    main()
