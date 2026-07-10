import time
import signal
import sys


from api.bybit_api import bybit_api

from risk.risk_manager import risk_manager

from execution.order_manager import order_manager

from execution.position_manager import position_manager

from signal.vwap_supertrend import vwap_supertrend

from websocket.public_ws import public_ws

from websocket.private_ws import private_ws


from config import (
    DEFAULT_SYMBOL,
    ORDER_COOLDOWN,
)



# ==========================================
# BOT MAIN
# ==========================================

class TradingBot:


    def __init__(self):


        self.running = False


        print("==============================")
        print("[APP INIT]")
        print("==============================")




    # ======================================
    # START
    # ======================================

    def start(self):


        print("==============================")
        print("VWAP SUPERTREND BOT START")
        print("==============================")


        # Risk 초기화

        try:

            risk_manager.initialize()


        except Exception as e:

            print(
                "[RISK INIT ERROR]",
                e
            )



        # Websocket 시작


        public_ws.run_thread()


        private_ws.run_thread()



        self.running = True



        print("[BOT RUNNING]")



        self.loop()





    # ======================================
    # MAIN LOOP
    # ======================================

    def loop(self):


        while self.running:


            try:



                candles = public_ws.get_candles()



                if len(candles) < 30:


                    time.sleep(1)

                    continue




                signal = vwap_supertrend.generate_signal(

                    candles

                )



                print(

                    "[SIGNAL]",

                    signal

                )




                # BUY

                if signal == "BUY":


                    order_manager.buy()



                # SELL

                elif signal == "SELL":


                    order_manager.sell()





                time.sleep(
                    ORDER_COOLDOWN
                )



            except Exception as e:


                print(

                    "[BOT LOOP ERROR]",

                    e

                )


                time.sleep(5)







    # ======================================
    # STOP
    # ======================================

    def stop(self):


        print()

        print("[BOT STOPPING]")



        self.running = False



        public_ws.stop()

        private_ws.stop()



        print("[BOT STOPPED]")







# ==========================================
# CTRL+C
# ==========================================

bot = TradingBot()



def shutdown(
    sig,
    frame
):


    bot.stop()

    sys.exit(0)



signal.signal(

    signal.SIGINT,

    shutdown

)



signal.signal(

    signal.SIGTERM,

    shutdown

)





# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":


    bot.start()
