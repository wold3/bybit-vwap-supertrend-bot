import time
import signal
import sys
import threading


from api.bybit_api import bybit_api

from risk.risk_manager import risk_manager

from execution.order_manager import order_manager

from execution.position_manager import PositionManager

from signals.vwap_supertrend import signal_engine

from ws.public_ws import public_ws

from ws.private_ws import private_ws



# ==========================================
# BOT APPLICATION
# ==========================================


class TradingBot:


    def __init__(self):


        self.running = False


        self.position_manager = PositionManager()


        self.prices = []

        self.volumes = []



        print("==============================")
        print("[APP INIT]")
        print("==============================")




    # ======================================
    # INITIALIZE
    # ======================================

    def initialize(self):


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


        except Exception:

            pass



        risk_manager.initialize(

            equity

        )



        public_ws.run_thread()

        private_ws.run_thread()



        time.sleep(2)




    # ======================================
    # MARKET UPDATE
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



            if len(self.prices) > 300:


                self.prices = self.prices[-300:]

                self.volumes = self.volumes[-300:]




    # ======================================
    # TRADING LOOP
    # ======================================

    def run_loop(self):


        print(
            "[BOT RUNNING]"
        )



        while self.running:


            try:


                self.update_market()



                if len(self.prices) < 30:


                    time.sleep(1)

                    continue




                signal = signal_engine.check_signal(

                    self.prices,

                    self.volumes

                )




                if signal == "Buy":


                    print(
                        "[SIGNAL] LONG"
                    )


                    order_manager.buy()




                elif signal == "Sell":


                    print(
                        "[SIGNAL] SHORT"
                    )


                    order_manager.sell()




                time.sleep(1)




            except Exception as e:


                print(
                    "[MAIN LOOP ERROR]",
                    e
                )


                time.sleep(2)




    # ======================================
    # START
    # ======================================

    def start(self):


        self.initialize()


        self.running = True


        self.run_loop()




    # ======================================
    # STOP
    # ======================================

    def stop(self):


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
# GLOBAL
# ==========================================


bot = TradingBot()




def shutdown_handler(
    sig,
    frame
):


    bot.stop()

    sys.exit(0)




signal.signal(

    signal.SIGINT,

    shutdown_handler

)


signal.signal(

    signal.SIGTERM,

    shutdown_handler

)




# ==========================================
# RUN
# ==========================================


if __name__ == "__main__":


    bot.start()
