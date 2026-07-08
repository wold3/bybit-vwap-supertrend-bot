import os
import time
import threading
import signal


from dotenv import load_dotenv


from services.ws_client import ws_client

from services.private_ws import private_ws


from strategy.strategy_engine import strategy_engine

from execution.execution_engine import execution_engine


from risk.drawdown_guard import drawdown_guard


from watchdog.watchdog import watchdog



load_dotenv()



running = True


last_signal = None


# =====================================
# PUBLIC WS
# =====================================

def public_ws_loop():


    print(

        "[START] PUBLIC WS"

    )


    ws_client.start()





# =====================================
# PRIVATE WS
# =====================================

def private_ws_loop():


    print(

        "[START] PRIVATE WS"

    )


    private_ws.start()





# =====================================
# STRATEGY LOOP
# =====================================

def strategy_loop():

    global last_signal
    
    print(

        "[START] STRATEGY LOOP"

    )



    while running:


        try:


            market_data = ws_client.get_latest_data()



            if not market_data:


                time.sleep(1)

                continue



            signal_data = strategy_engine.check(

                market_data

            )



            if signal_data:

                signal_key = (
                    signal_data.get("type"),
                    signal_data.get("symbol"),
                    signal_data.get("side")
                )


                if signal_key == last_signal:

                    continue


                last_signal = signal_key


                print(
                    "[SIGNAL]",
                    signal_data
                )


                result = execution_engine.execute_signal(

                    signal_data

                )


                print(
                    "[EXECUTION]",
                    result
                )


        except Exception as e:


            print(

                "[STRATEGY ERROR]",

                e

            )



        time.sleep(1)





# =====================================
# EQUITY MONITOR
# =====================================

def equity_loop():


    print(

        "[START] EQUITY LOOP"

    )



    while running:


        try:


            equity = execution_engine.get_account_equity()



            if equity > 0:


                drawdown_guard.update(

                    equity

                )


                print(

                    "[EQUITY]",

                    equity

                )



        except Exception as e:


            print(

                "[EQUITY ERROR]",

                e

            )



        time.sleep(10)





# =====================================
# THREAD START
# =====================================

def start_thread(
    func
):


    thread = threading.Thread(

        target=func,

        daemon=True

    )


    thread.start()


    return thread





# =====================================
# SHUTDOWN
# =====================================

def shutdown(
    signum=None,
    frame=None
):


    global running


    print(

        "\n[BOT STOPPING]"

    )


    running = False



    try:


        ws_client.stop()


    except:


        pass



    try:


        private_ws.stop()


    except:


        pass



    try:


        watchdog.stop()


    except:


        pass



    print(

        "[BOT STOPPED]"

    )





# =====================================
# MAIN
# =====================================

if __name__ == "__main__":



    print(

        """

====================================

🚀 BYBIT AI TRADING BOT

MODE : {}

SYMBOL : {}

====================================

""".format(

            os.getenv(

                "LIVE_TRADING",

                "false"

            ),

            os.getenv(

                "DEFAULT_SYMBOL",

                "BTCUSDT"

            )

        )

    )




    # Watchdog FIRST

    watchdog.start()



    signal.signal(

        signal.SIGINT,

        shutdown

    )


    signal.signal(

        signal.SIGTERM,

        shutdown

    )





    threads = []



    services = [


        public_ws_loop,


        private_ws_loop,


        strategy_loop,


        equity_loop


    ]



    for service in services:


        threads.append(

            start_thread(

                service

            )

        )





    try:


        while running:


            time.sleep(1)



    except KeyboardInterrupt:


        shutdown()
