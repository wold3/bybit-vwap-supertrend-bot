# main.py

import os
import time
import threading
import signal


from dotenv import load_dotenv


from services.ws_client import ws_client

from services.private_ws import private_ws


from strategy.strategy_engine import strategy_engine

from execution.execution_engine import execution_engine


from position.position_manager import position_manager


from risk.drawdown_guard import drawdown_guard

from risk.risk_engine import risk_engine


from watchdog.watchdog import watchdog



load_dotenv()



running = True





# =====================================
# PUBLIC WS
# =====================================

def public_ws_loop():


    print(

        "[START] PUBLIC WS"

    )


    ws_client.start()



    while running:


        watchdog.heartbeat(

            "public_ws"

        )


        time.sleep(5)





# =====================================
# PRIVATE WS
# =====================================

def private_ws_loop():


    print(

        "[START] PRIVATE WS"

    )


    private_ws.start()



    while running:


        watchdog.heartbeat(

            "private_ws"

        )


        time.sleep(5)





# =====================================
# STRATEGY
# =====================================

def strategy_loop():


    print(

        "[START] STRATEGY LOOP"

    )



    while running:


        try:


            watchdog.heartbeat(

                "strategy"

            )



            market_data = (

                ws_client

                .get_latest_data()

            )



            if not market_data:


                time.sleep(1)

                continue





            signal_data = strategy_engine.check(

                market_data

            )



            if signal_data:


                print(

                    "[SIGNAL]",

                    signal_data

                )



                result = execution_engine.execute_signal(

                    signal_data

                )



                print(

                    "[EXEC RESULT]",

                    result

                )



        except Exception as e:


            print(

                "[STRATEGY ERROR]",

                e

            )



        time.sleep(1)





# =====================================
# EQUITY
# =====================================

def equity_loop():


    print(

        "[START] EQUITY LOOP"

    )



    while running:


        try:


            watchdog.heartbeat(

                "equity"

            )



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
    target
):


    thread = threading.Thread(

        target=target,

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

        "\n[SHUTDOWN]"

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



    watchdog.stop()



    print(

        "BOT STOPPED"

    )





signal.signal(

    signal.SIGINT,

    shutdown

)


signal.signal(

    signal.SIGTERM,

    shutdown

)





# =====================================
# MAIN
# =====================================

if __name__ == "__main__":


    mode = os.getenv(

        "LIVE_TRADING",

        "false"

    )



    print(

        """

=====================================

🚀 BYBIT AI TRADING BOT

MODE : {}

=====================================

""".format(

            mode

        )

    )





    watchdog.start()



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
