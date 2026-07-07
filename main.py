import os
import time
import threading


from dotenv import load_dotenv

load_dotenv()



# ===============================
# SERVICES
# ===============================

from services.ws_client import ws_client

from services.private_ws import private_ws



# ===============================
# STRATEGY / EXECUTION
# ===============================

from strategy.strategy_engine import strategy_engine

from execution.execution_engine import execution_engine



# ===============================
# POSITION / RISK
# ===============================

from position.position_manager import position_manager

from risk.drawdown_guard import drawdown_guard



# ===============================
# WATCHDOG
# ===============================

from watchdog.watchdog import watchdog





running = True





# =====================================
# PUBLIC WS
# =====================================

def public_ws_loop():


    print(

        "START PUBLIC WS"

    )


    ws_client.start()





# =====================================
# PRIVATE WS
# =====================================

def private_ws_loop():


    print(

        "START PRIVATE WS"

    )


    private_ws.start()





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



            if not signal:


                time.sleep(1)

                continue





            print(

                "SIGNAL",

                signal

            )





            # ==========================
            # ENTRY
            # ==========================

            if signal["type"] == "ENTRY":


                result = execution_engine.execute(

                    symbol=

                    signal["symbol"],


                    side=

                    signal["side"],


                    qty=

                    signal["qty"]

                )



                print(

                    "ENTRY RESULT",

                    result

                )





            # ==========================
            # EXIT
            # ==========================

            elif signal["type"] == "EXIT":



                position = (

                    position_manager
                    .get_position(

                        signal["symbol"]

                    )

                )



                if position:


                    result = execution_engine.close_position(

                        symbol=

                        signal["symbol"],


                        side=

                        position["side"],


                        qty=

                        position["size"]

                    )



                    print(

                        "EXIT RESULT",

                        result

                    )





        except Exception as e:


            print(

                "STRATEGY ERROR",

                e

            )



        time.sleep(1)







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

                    "EQUITY",

                    equity

                )



        except Exception as e:


            print(

                "EQUITY ERROR",

                e

            )



        time.sleep(10)





# =====================================
# WATCHDOG
# =====================================

def watchdog_loop():


    print(

        "START WATCHDOG"

    )


    watchdog.start()





# =====================================
# START THREAD
# =====================================

def start_thread(
    target
):


    t = threading.Thread(

        target=target,

        daemon=True

    )


    t.start()


    return t





# =====================================
# MAIN
# =====================================

if __name__ == "__main__":


    print(

        """

====================================

🚀 BYBIT AI TRADING BOT START

MODE:

{}

====================================

""".format(

            os.getenv(

                "LIVE_TRADING",

                "false"

            )

        )

    )



    threads = []



    services = [


        public_ws_loop,


        private_ws_loop,


        strategy_loop,


        equity_loop,


        watchdog_loop


    ]



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


        running = False



        watchdog.stop()



        print(

            "BOT STOPPED"

        )
