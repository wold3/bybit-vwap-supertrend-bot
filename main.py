import time
import signal
import sys


from config import (
    LIVE_TRADING,
    DEFAULT_SYMBOL,
    BYBIT_BASE_URL
)


from market.websocket_client import (
    ws_client
)


from services.private_ws_client import (
    private_ws_client
)


from portfolio.bybit_wallet import (
    wallet
)


from watchdog import (
    watchdog
)



running = True



# ==================================
# STOP HANDLER
# ==================================

def shutdown(
    signum=None,
    frame=None
):

    global running


    print()

    print(
        "[BOT STOPPING]"
    )


    running = False



    try:

        ws_client.stop()

    except Exception as e:

        print(
            "[PUBLIC STOP ERROR]",
            e
        )



    try:

        private_ws_client.stop()

    except Exception as e:

        print(
            "[PRIVATE STOP ERROR]",
            e
        )



    try:

        watchdog.stop()

    except Exception:

        pass



    print(
        "[BOT STOPPED]"
    )


    sys.exit(0)





signal.signal(
    signal.SIGINT,
    shutdown
)


signal.signal(
    signal.SIGTERM,
    shutdown
)





# ==================================
# START
# ==================================

def main():


    print("====================================")
    print("VWAP SUPERTREND BOT START")
    print("LIVE :", LIVE_TRADING)
    print("SYMBOL :", DEFAULT_SYMBOL)
    print("BASE :", BYBIT_BASE_URL)
    print("====================================")



    # watchdog 1회

    try:

        watchdog.start()

    except Exception as e:

        print(
            "[WATCHDOG ERROR]",
            e
        )



    # public market websocket

    print(
        "[START] PUBLIC WS"
    )


    ws_client.start()



    time.sleep(2)



    # private account websocket

    print(
        "[START] PRIVATE WS"
    )


    private_ws_client.start()



    time.sleep(3)



    # wallet check

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



    print(
        "[START] STRATEGY LOOP"
    )


    print(
        "[BOT RUNNING]"
    )



    while running:


        try:

            time.sleep(1)


        except KeyboardInterrupt:


            shutdown()





if __name__ == "__main__":


    main()
