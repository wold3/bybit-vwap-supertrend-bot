# main.py

import time
import signal

from dotenv import load_dotenv


# =====================================
# LOAD ENV FIRST
# =====================================

load_dotenv()



# =====================================
# CONFIG
# =====================================

from config import (
    DEFAULT_SYMBOL,
    LIVE_TRADING,
    BYBIT_BASE_URL,
)



# =====================================
# SERVICES
# =====================================

from services.ws_client import (
    ws_client
)


from services.private_ws_client import (
    private_ws_client
)



# =====================================
# PORTFOLIO
# =====================================

from portfolio.bybit_wallet import (
    wallet
)



# =====================================
# WATCHDOG
# =====================================

from watchdog.watchdog import (
    watchdog
)



# =====================================
# GLOBAL STATE
# =====================================

RUNNING = True



# =====================================
# SHUTDOWN
# =====================================

def shutdown(
    signum=None,
    frame=None
):

    global RUNNING


    if not RUNNING:
        return



    RUNNING = False



    print()

    print(
        "[BOT STOPPING]"
    )



    # public ws stop

    try:

        ws_client.stop()


    except Exception as e:

        print(
            "[PUBLIC STOP ERROR]",
            e
        )



    # private ws stop

    try:

        private_ws_client.stop()


    except Exception as e:

        print(
            "[PRIVATE STOP ERROR]",
            e
        )



    # watchdog stop

    try:

        watchdog.stop()


    except Exception as e:

        print(
            "[WATCHDOG STOP ERROR]",
            e
        )



    print(
        "[BOT STOPPED]"
    )




# =====================================
# SIGNAL
# =====================================

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

def main():


    print(
        "===================================="
    )

    print(
        "VWAP SUPERTREND BOT START"
    )

    print(
        "LIVE :",
        LIVE_TRADING
    )

    print(
        "SYMBOL :",
        DEFAULT_SYMBOL
    )

    print(
        "BASE :",
        BYBIT_BASE_URL
    )

    print(
        "===================================="
    )



    # -----------------------------
    # WATCHDOG
    # -----------------------------

    try:

        watchdog.start()


        print(
            "[WATCHDOG START]"
        )


    except Exception as e:

        print(
            "[WATCHDOG ERROR]",
            e
        )



    # -----------------------------
    # PUBLIC WS
    # -----------------------------

    print(
        "[START] PUBLIC WS"
    )


    try:

        ws_client.start()


    except Exception as e:

        print(
            "[PUBLIC WS ERROR]",
            e
        )



    time.sleep(2)



    # -----------------------------
    # PRIVATE WS
    # -----------------------------

    print(
        "[START] PRIVATE WS"
    )


    try:

        private_ws_client.start()


    except Exception as e:

        print(
            "[PRIVATE WS ERROR]",
            e
        )



    time.sleep(3)



    # -----------------------------
    # WALLET CHECK
    # -----------------------------

    try:

        equity = wallet.get_equity()


        print(
            "[ACCOUNT EQUITY]",
            equity
        )


    except Exception as e:

        print(
            "[WALLET ERROR]",
            e
        )



    # -----------------------------
    # STRATEGY LOOP
    # -----------------------------

    print(
        "[START] STRATEGY LOOP"
    )



    while RUNNING:


        time.sleep(1)




# =====================================
# ENTRY
# =====================================

if __name__ == "__main__":

    main()
