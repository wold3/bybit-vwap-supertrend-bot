import time
import signal
import threading


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



def shutdown(
    sig=None,
    frame=None
):

    global running


    print()
    print("[BOT STOPPING]")


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



    raise SystemExit




signal.signal(
    signal.SIGINT,
    shutdown
)


signal.signal(
    signal.SIGTERM,
    shutdown
)




def equity_loop():


    while running:


        try:


            equity = (
                wallet.get_equity()
            )


            print(
                "[ACCOUNT EQUITY]",
                equity
            )



        except Exception as e:


            print(
                "[EQUITY ERROR]",
                e
            )



        time.sleep(
            30
        )




def strategy_loop():


    print(
        "[START] STRATEGY LOOP"
    )


    while running:


        time.sleep(
            1
        )




def main():


    print("====================================")
    print("VWAP SUPERTREND BOT START")
    print("LIVE :", LIVE_TRADING)
    print("SYMBOL :", DEFAULT_SYMBOL)
    print("BASE :", BYBIT_BASE_URL)
    print("====================================")



    # watchdog

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



    # public websocket

    print(
        "[START] PUBLIC WS"
    )


    ws_client.start()



    time.sleep(
        2
    )



    # private websocket

    print(
        "[START] PRIVATE WS"
    )


    private_ws_client.start()



    time.sleep(
        2
    )



    # equity thread

    threading.Thread(

        target=equity_loop,

        daemon=True

    ).start()



    # strategy thread

    threading.Thread(

        target=strategy_loop,

        daemon=True

    ).start()



    print(
        "[BOT RUNNING]"
    )



    while running:


        time.sleep(
            1
        )





if __name__ == "__main__":


    main()
