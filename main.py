# =====================================================
# main.py
# Bybit VWAP SuperTrend Bot
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


        print(

            "\n[USER STOP]"

        )


        app.stop()



    except Exception as e:


        print(

            "[MAIN ERROR]",

            e

        )


        traceback.print_exc()



        try:


            app.stop()


        except:


            pass







if __name__ == "__main__":


    main()
