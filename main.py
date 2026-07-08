# main.py

import os
import time
import threading


from dotenv import load_dotenv


load_dotenv()



# =====================================
# SERVICES
# =====================================

from services.ws_client import ws_client

from services.private_ws import private_ws



# =====================================
# STRATEGY / EXECUTION
# =====================================

from strategy.strategy_engine import strategy_engine

from execution.execution_engine import execution_engine



# =====================================
# RISK / POSITION
# =====================================

from risk.drawdown_guard import drawdown_guard

from position.position_manager import position_manager



# =====================================
# WATCHDOG
# =====================================

from watchdog.watchdog import watchdog





running = True





# =====================================
# WATCHDOG LOOP
# =====================================

def watchdog_loop():

    print(
        "START WATCHDOG"
    )


    watchdog.start()


    while running:


        try:

            watchdog.heartbeat()


        except Exception as e:

            print(
                "[WATCHDOG ERROR]",
                e
            )


        time.sleep(5)





# =====================================
# PUBLIC WS LOOP
# =====================================

def public_ws_loop():

    print(
        "START PUBLIC WS"
    )


    ws_client.start()


    while running:


        try:

            watchdog.heartbeat()


        except Exception as e:

            print(
                "[PUBLIC WS LOOP ERROR]",
                e
            )


        time.sleep(5)





# =====================================
# PRIVATE WS LOOP
# =====================================

def private_ws_loop():

    print(
        "START PRIVATE WS"
    )


    private_ws.start()


    while running:


        try:

            watchdog.heartbeat()


        except Exception as e:

            print(
                "[PRIVATE WS LOOP ERROR]",
                e
            )


        time.sleep(5)





# =====================================
# EQUITY LOOP
# =====================================

def equity_loop():

    print(
        "START EQUITY LOOP"
    )


    while running:


        try:


            equity = (

                execution_engine
                .get_account_equity()

            )


            if equity > 0:


                drawdown_guard.update(

                    equity

                )


                print(

                    "[EQUITY]",

                    equity

                )



            watchdog.heartbeat()



        except Exception as e:


            print(

                "[EQUITY ERROR]",

                e

            )



        time.sleep(10)





# =====================================
# STRATEGY LOOP
# =====================================

def strategy_loop():

    print(
        "START STRATEGY LOOP"
    )


    while running:


        try:


            market_data = (

                ws_client
                .get_latest_data()

            )



            if not market_data:


                time.sleep(1)

                continue





            signal = strategy_engine.check(

                market_data

            )



            if signal:


                print(

                    "[SIGNAL]",

                    signal

                )


                result = execution_engine.execute_signal(

                    signal

                )


                print(

                    "[EXECUTION RESULT]",

                    result

                )



            watchdog.heartbeat()



        except Exception as e:


            print(

                "[STRATEGY ERROR]",

                e

            )



        time.sleep(1)





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
# STOP
# =====================================

def shutdown():


    global running


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

        "BOT STOPPED"

    )





# =====================================
# MAIN
# =====================================

if __name__ == "__main__":



    print(
        """

====================================

🚀 BYBIT AI TRADING BOT START

MODE : {}

====================================

""".format(

            os.getenv(

                "LIVE_TRADING",

                "false"

            )

        )

    )



    services = [

        # 1순위
        watchdog_loop,


        # 시장 데이터
        public_ws_loop,


        # 계좌/체결 동기화
        private_ws_loop,


        # 리스크 관리
        equity_loop,


        # 최종 판단
        strategy_loop

    ]



    threads = []



    for service in services:


        threads.append(

            start_thread(

                service

            )

        )





    try:


        while True:


            time.sleep(1)



    except KeyboardInterrupt:


        shutdown()
