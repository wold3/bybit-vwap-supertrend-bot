import time
import signal as os_signal


from api.bybit_api import bybit_api

from risk.risk_manager import risk_manager

from execution.order_manager import order_manager

from execution.position_manager import position_manager

from signals.vwap_supertrend import signal_engine

from ws.public_ws import public_ws

from ws.private_ws import private_ws



# ==========================================
# TRADING BOT
# ==========================================

class TradingBot:


    def __init__(self):

        print("==============================")
        print("[APP INIT]")
        print("==============================")


        self.running = True



    # ======================================
    # START
    # ======================================

    def start(self):


        print("====================================")
        print("VWAP SUPERTREND BOT START")
        print("====================================")



        # --------------------------
        # Risk Initialize
        # --------------------------

        try:

            risk_manager.initialize(
                bybit_api.get_wallet_balance()
            )


        except Exception as e:

            print(
                "[RISK INIT ERROR]",
                e
            )



        # --------------------------
        # Websocket Start
        # --------------------------

        try:

            public_ws.run_thread()

            private_ws.run_thread()


        except Exception as e:

            print(
                "[WS START ERROR]",
                e
            )



        print("[BOT RUNNING]")



        while self.running:


            try:

                self.loop()


            except Exception as e:

                print(
                    "[MAIN LOOP ERROR]",
                    e
                )


            time.sleep(1)



    # ======================================
    # MAIN LOOP
    # ======================================

    def loop(self):


        candles = public_ws.get_candles()



        if candles is None:

            return



        signal = signal_engine.check_signal(

            candles

        )



        if signal is None:

            return



        print("==============================")
        print("[TRADING SIGNAL]")
        print(signal)
        print("==============================")



        if signal == "BUY":


            order_manager.buy()



        elif signal == "SELL":


            order_manager.sell()




    # ======================================
    # STOP
    # ======================================

    def stop(self):


        print("[BOT STOPPING]")


        self.running = False



        try:

            public_ws.stop()

            private_ws.stop()


        except Exception as e:

            print(
                "[STOP ERROR]",
                e
            )



        print("[BOT STOPPED]")




# ==========================================
# INSTANCE
# ==========================================

bot = TradingBot()



# ==========================================
# SYSTEM SIGNAL HANDLER
# ==========================================

def shutdown_handler(

        signum,

        frame

):

    bot.stop()



os_signal.signal(

    os_signal.SIGINT,

    shutdown_handler

)



os_signal.signal(

    os_signal.SIGTERM,

    shutdown_handler

)




# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    bot.start()
