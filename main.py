import time
import signal
import traceback


from api.bybit_api import bybit_api

from ws.public_ws import public_ws
from ws.private_ws import private_ws

from signals.vwap_supertrend import signal_engine

from execution.order_manager import order_manager
from execution.position_manager import position_manager

from risk.risk_manager import risk_manager





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



        # --------------------------
        # WALLET
        # --------------------------

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





        # --------------------------
        # LEVERAGE
        # --------------------------

        try:


            bybit_api.set_leverage()



        except Exception as e:


            print(
                "[LEVERAGE ERROR]",
                e
            )





        # --------------------------
        # WS START
        # --------------------------

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


                traceback.print_exc()



            time.sleep(1)





    # ======================================
    # LOOP
    # ======================================

    def loop(self):


        (
            opens,
            highs,
            lows,
            closes,
            volumes

        ) = public_ws.get_ohlcv()



        if len(closes) < 20:


            return





        print(
            "[DATA]",
            len(closes)
        )





        # --------------------------
        # POSITION EXIT
        # --------------------------

        if position_manager.has_position():


            exit_signal = (

                position_manager.check_exit(

                    closes[-1]

                )

            )



            if exit_signal:


                print(
                    "[EXIT]",
                    exit_signal
                )


                order_manager.close_position()



                return





        # --------------------------
        # RISK CHECK
        # --------------------------

        if not risk_manager.can_trade():


            return





        # --------------------------
        # DUPLICATE POSITION
        # --------------------------

        if order_manager.has_position():


            return





        # --------------------------
        # SIGNAL
        # --------------------------

        result = signal_engine.check_signal(

            close=closes,

            volume=volumes,

            high=highs,

            low=lows

        )





        if result:


            print(
                "[SIGNAL]",
                result
            )





            if result == "Buy":


                order_manager.buy()





            elif result == "Sell":


                order_manager.sell()






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



def shutdown(signum, frame):


    app.stop()



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


    try:


        app.start()



    except KeyboardInterrupt:


        app.stop()



    except Exception as e:


        print(
            "[FATAL ERROR]",
            e
        )


        traceback.print_exc()


        app.stop()
