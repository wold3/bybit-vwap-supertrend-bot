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



from strategy.strategy_engine import (
    strategy_engine
)





running = True





# ==================================
# CANDLE CALLBACK
# ==================================

def candle_handler(candle):


    print(
        "[CANDLE]",
        candle
    )


    try:

        strategy_engine.on_candle(
            candle
        )


    except Exception as e:


        print(
            "[STRATEGY ERROR]",
            e
        )





# ==================================
# STOP
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

    except:

        pass



    try:

        private_ws_client.stop()

    except:

        pass



    try:

        watchdog.stop()

    except:

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
# MAIN
# ==================================

def main():


    print("====================================")
    print("VWAP SUPERTREND BOT START")
    print("LIVE :", LIVE_TRADING)
    print("SYMBOL :", DEFAULT_SYMBOL)
    print("BASE :", BYBIT_BASE_URL)
    print("====================================")



    #
    # candle callback 연결
    #

    try:

        ws_client.set_callback(
            candle_handler
        )


    except Exception as e:


        print(
            "[CALLBACK ERROR]",
            e
        )





    watchdog.start()



    print(
        "[START] PUBLIC WS"
    )


    ws_client.start()



    time.sleep(2)



    print(
        "[START] PRIVATE WS"
    )


    private_ws_client.start()



    time.sleep(3)





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


        time.sleep(1)






if __name__ == "__main__":


    main()
