import time
import signal as system_signal
import sys


from api.bybit_api import bybit_api

from risk.risk_manager import risk_manager

from execution.order_manager import order_manager

from execution.position_manager import PositionManager

from signals.vwap_supertrend import signal_engine

from ws.public_ws import public_ws

from ws.private_ws import private_ws



# ==========================================
# TRADING BOT
# ==========================================

class TradingBot:


    def __init__(self):

        self.running = False

        self.prices = []

        self.volumes = []

        self.position_manager = PositionManager()


        print("==============================")
        print("[APP INIT]")
        print("==============================")



    # ======================================
    # INITIALIZE
    # ======================================

    def initialize(self):

        print()
        print("====================================")
        print("VWAP SUPERTREND BOT START")
        print("====================================")


        wallet = bybit_api.get_wallet_balance()


        equity = 0


        try:

            equity = float(

                wallet["result"]
                ["list"][0]
                ["totalEquity"]

            )


        except Exception as e:

            print(
                "[EQUITY ERROR]",
                e
            )



        risk_manager.initialize(
            equity
        )



        public_ws.run_thread()

        private_ws.run_thread()



        time.sleep(3)



    # ======================================
    # MARKET DATA
    # ======================================

    def update_market(self):


        price = public_ws.get_price()



        if price:


            self.prices.append(

                price

            )


            self.volumes.append(

                1

            )


            print(
                "[PRICE]",
                price
            )



            if len(self.prices) > 300:


                self.prices = self.prices[-300:]

                self.volumes = self.volumes[-300:]




    # ======================================
    # SIGNAL PROCESS
    # ======================================

    def process_signal(self):


        if len(self.prices) < 30:

            return



        signal = signal_engine.check_signal(

            self.prices,

            self.volumes

        )



        if signal == "Buy":


            print(
                "[SIGNAL] BUY"
            )


            order_manager.buy()



        elif signal == "Sell":


            print(
                "[SIGNAL] SELL"
            )


            order_manager.sell()




    # ======================================
    # LOOP
    # ======================================

    def run(self):


        self.running = True


        print(
            "[BOT RUNNING]"
        )



        while self.running:


            try:


                self.update_market()


                self.process_signal()


                time.sleep(1)



            except Exception as e:


                print(
                    "[MAIN LOOP ERROR]",
                    e
                )


                time.sleep(2)




    # ======================================
    # STOP
    # ======================================

    def stop(self):


        if not self.running:

            return



        print(
            "[BOT STOPPING]"
        )



        self.running = False



        public_ws.stop()

        private_ws.stop()



        print(
            "[BOT STOPPED]"
        )





# ==========================================
# GLOBAL BOT
# ==========================================

bot = TradingBot()



# ==========================================
# SHUTDOWN HANDLER
# ==========================================

def shutdown_handler(
    signum,
    frame
):

    bot.stop()

    sys.exit(0)




system_signal.signal(

    system_signal.SIGINT,

    shutdown_handler

)


system_signal.signal(

    system_signal.SIGTERM,

    shutdown_handler

)



# ==========================================
# START
# ==========================================

if __name__ == "__main__":


    try:

        bot.initialize()

        bot.run()



    except KeyboardInterrupt:


        bot.stop()
