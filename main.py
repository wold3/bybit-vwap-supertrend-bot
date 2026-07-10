import time
import signal as system_signal
import sys


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

        self.running = False

        self.prices = []

        self.volumes = []

        self.entry_price = None

        self.position_side = None



        print("==============================")
        print("[APP INIT]")
        print("==============================")



    # ======================================
    # STARTUP
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


        except:

            pass



        risk_manager.initialize(

            equity

        )



        bybit_api.set_leverage()



        public_ws.run_thread()

        private_ws.run_thread()



        time.sleep(3)




    # ======================================
    # PRICE UPDATE
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
    # POSITION STATUS
    # ======================================

    def update_position(self):


        try:


            pos = private_ws.get_position()



            if not pos:

                return



            data = pos.get(
                "data",
                {}
            )



        except Exception:

            pass




    # ======================================
    # ENTRY CHECK
    # ======================================

    def check_entry(self):


        if len(self.prices) < 30:

            return



        if order_manager.has_position():

            return



        signal = signal_engine.check_signal(

            self.prices,

            self.volumes

        )



        if signal == "Buy":


            print(
                "[SIGNAL] BUY"
            )


            result = order_manager.buy()



            if result:


                self.position_side = "Buy"

                self.entry_price = self.prices[-1]




        elif signal == "Sell":


            print(
                "[SIGNAL] SELL"
            )


            result = order_manager.sell()



            if result:


                self.position_side = "Sell"

                self.entry_price = self.prices[-1]




    # ======================================
    # EXIT CHECK
    # ======================================

    def check_exit(self):


        if not self.entry_price:

            return



        if not self.position_side:

            return



        result = position_manager.evaluate_exit(

            self.entry_price,

            self.position_side,

            self.prices

        )



        if result:


            print(
                "[EXIT]",
                result
            )


            bybit_api.cancel_all_orders()



            self.entry_price = None

            self.position_side = None




    # ======================================
    # MAIN LOOP
    # ======================================

    def run(self):


        self.running = True


        print(
            "[BOT RUNNING]"
        )



        while self.running:


            try:


                self.update_market()


                self.check_exit()


                self.check_entry()



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
# RUN
# ==========================================

bot = TradingBot()



def shutdown(
    sig,
    frame
):

    bot.stop()

    sys.exit(0)




system_signal.signal(

    system_signal.SIGINT,

    shutdown

)


system_signal.signal(

    system_signal.SIGTERM,

    shutdown

)




if __name__ == "__main__":


    bot.initialize()

    bot.run()
