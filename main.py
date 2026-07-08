import os
import time
import signal
import threading

from dotenv import load_dotenv


load_dotenv()



from services.ws_client import ws_client
from services.private_ws_client import private_ws_client

from portfolio.bybit_wallet import wallet

from watchdog.watchdog import watchdog





# =====================================
# GLOBAL
# =====================================

running = True






# =====================================
# STRATEGY LOOP
# =====================================

def strategy_loop():


    print(
        "[START] STRATEGY LOOP"
    )


    while running:


        try:


            data = ws_client.get_latest_data()


            if data:


                pass



        except Exception as e:


            print(
                "[STRATEGY LOOP ERROR]",
                e
            )


        time.sleep(1)








# =====================================
# EQUITY LOOP
# =====================================

def equity_loop():


    print(
        "[START] EQUITY LOOP"
    )


    while running:


        try:


            equity = wallet.get_equity()


            if equity:


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
# SHUTDOWN
# =====================================

def shutdown(
    sig=None,
    frame=None
):


    global running


    print(
        "\n[BOT STOPPING]"
    )


    running = False



    try:

        ws_client.stop()

    except Exception:

        pass



    try:

        private_ws_client.stop()

    except Exception:

        pass



    try:

        watchdog.stop()

    except Exception:

        pass



    print(
        "[BOT STOPPED]"
    )









# =====================================
# START
# =====================================

def start():


    print(
        "===================================="
    )


    print(
        "VWAP SUPERTREND BOT START"
    )


    print(
        "LIVE :",
        os.getenv(
            "LIVE_TRADING",
            "false"
        )
    )


    print(
        "SYMBOL :",
        os.getenv(
            "DEFAULT_SYMBOL",
            "BTCUSDT"
        )
    )


    print(
        "===================================="
    )





    signal.signal(
        signal.SIGINT,
        shutdown
    )


    signal.signal(
        signal.SIGTERM,
        shutdown
    )






    # =================================
    # WATCHDOG
    # =================================

    watchdog.start()






    # =================================
    # PUBLIC WS
    # =================================

    print(
        "[START] PUBLIC WS"
    )


    ws_client.start()






    # =================================
    # PRIVATE WS
    # =================================

    print(
        "[START] PRIVATE WS"
    )


    private_ws_client.start()






    # =================================
    # STRATEGY THREAD
    # =================================

    threading.Thread(

        target=strategy_loop,

        daemon=True

    ).start()






    # =================================
    # EQUITY THREAD
    # =================================

    threading.Thread(

        target=equity_loop,

        daemon=True

    ).start()






    while running:


        time.sleep(1)









# =====================================
# ENTRY
# =====================================

if __name__ == "__main__":


    start()
