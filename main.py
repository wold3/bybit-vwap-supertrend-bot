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
# BOT CLASS
# ==========================================

class TradingBot:


    def __init__(self):

        self.running = False

        self.entry_price = None

        self.position_side = None


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



        bybit_api.set_leverage()



        public_ws.run_thread()

        private_ws.run_thread()



        time.sleep(3)




    # ======================================
    # ENTRY
    # ======================================

    def check_entry(self):


        try:


            opens, highs, lows, closes, volumes = (
                public_ws.get_ohlcv()
            )



            if len(closes) < 30:

                return




            if order_manager.has_position():

                return




            signal = signal_engine.check_signal(

                closes,

                volumes,

                highs,

                lows,

                closes

            )



            if signal == "Buy":


                print(
                    "[SIGNAL] BUY"
                )


                result = order_manager.buy()



                if result:


                    self.position_side = "Buy"

                    self.entry_price = closes[-1]




            elif signal == "Sell":


                print(
                    "[SIGNAL] SELL"
                )


                result = order_manager.sell()



                if result:


                    self.position_side = "Sell"

                    self.entry_price = closes[-1]




        except Exception as e:


            print(
                "[ENTRY ERROR]",
                e
            )




    # ======================================
    # EXIT
    # ======================================

    def check_exit(self):


        try:


            if self.entry_price is None:

                return



            if self.position_side is None:

                return




            _, _, _, closes, _ = public_ws.get_ohlcv()



            if len(closes) < 20:

                return




            result = position_manager.evaluate_exit(

                self.entry_price,

                self.position_side,

                closes

            )



            if result:


                print(
                    "[EXIT SIGNAL]",
                    result
                )



                bybit_api.cancel_all_orders()



                self.entry_price = None

                self.position_side = None




        except Exception as e:


            print(
                "[EXIT ERROR]",
                e
            )




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
# INSTANCE
# ==========================================

bot = TradingBot()




# ==========================================
# SIGNAL HANDLER
# ==========================================

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




# ==========================================
# START
# ==========================================

if __name__ == "__main__":


    try:


        bot.initialize()

        bot.run()



    except KeyboardInterrupt:


        bot.stop()
