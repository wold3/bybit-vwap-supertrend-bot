import time
import signal
import threading


from api.bybit_api import bybit_api

from ws.public_ws import public_ws
from ws.private_ws import private_ws

from signals.vwap_supertrend import signal_engine

from execution.order_manager import order_manager
from execution.position_manager import position_manager

from risk.risk_manager import risk_manager


from config import (
    DEFAULT_QTY,
)



# ==========================================
# BOT APPLICATION
# ==========================================

class BotApp:


    def __init__(self):


        self.running = False



        print("==============================")
        print("[APP INIT]")
        print("==============================")





    # ======================================
    # START
    # ======================================

    def start(self):


        print()
        print("====================================")
        print("VWAP SUPERTREND BOT START")
        print("====================================")



        # ------------------------------
        # WALLET
        # ------------------------------

        wallet = bybit_api.get_wallet_balance()



        if wallet:


            try:


                equity = float(

                    wallet["result"]
                    ["list"][0]
                    ["totalEquity"]

                )


                risk_manager.initialize(

                    equity

                )


            except Exception as e:


                print(
                    "[RISK INIT ERROR]",
                    e
                )





        # ------------------------------
        # LEVERAGE
        # ------------------------------

        try:


            bybit_api.set_leverage()



        except Exception as e:


            print(
                "[LEVERAGE ERROR]",
                e
            )





        # ------------------------------
        # WS START
        # ------------------------------

        public_ws.run_thread()

        private_ws.run_thread()



        print(
            "[WS THREADS STARTED]"
        )



        self.running = True



        print(
            "[BOT RUNNING]"
        )




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


        opens, highs, lows, closes, volumes = (

            public_ws.get_ohlcv()

        )



        if len(closes) < 20:


            return




        print(
            "[DATA]",
            len(closes)
        )





        # ------------------------------
        # EXIT CHECK
        # ------------------------------

        if position_manager.has_position():



            result = position_manager.evaluate_exit(

                position_manager.entry_price,

                position_manager.side,

                closes

            )



            if result:



                print(
                    "[EXIT]",
                    result
                )


                order_manager.close_position()

                position_manager.clear()



                return






        # ------------------------------
        # ENTRY CHECK
        # ------------------------------

        if not risk_manager.can_trade():


            return




        if order_manager.has_position():


            return





        signal_result = signal_engine.check_signal(

            close=closes,

            volume=volumes,

            high=highs,

            low=lows

        )



        if signal_result:


            print(
                "[SIGNAL]",
                signal_result
            )



            if signal_result == "Buy":


                if order_manager.buy():


                    position_manager.update_position(

                        "Buy",

                        DEFAULT_QTY,

                        closes[-1]

                    )




            elif signal_result == "Sell":


                if order_manager.sell():


                    position_manager.update_position(

                        "Sell",

                        DEFAULT_QTY,

                        closes[-1]

                    )





    # ======================================
    # STOP
    # ======================================

    def stop(self):


        print()

        print(
            "[SHUTDOWN]"
        )



        self.running = False



        public_ws.stop()

        private_ws.stop()



        print(
            "[BOT STOPPED]"
        )






# ==========================================
# SIGNAL HANDLER
# ==========================================

app = BotApp()



def shutdown_handler(

    signum,

    frame

):


    app.stop()



    raise SystemExit





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


    app.start()
