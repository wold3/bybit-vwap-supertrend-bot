import time
import signal
import threading


from config import (
    LIVE_TRADING,
    DEFAULT_SYMBOL,
    BYBIT_BASE_URL
)


from market.websocket_client import websocket_client
from services.private_ws_client import private_ws_client
from portfolio.bybit_wallet import wallet

from execution.order_manager import order_manager

from strategy.strategy_engine import (
    strategy_engine
)


from indicators.vwap import calculate_vwap
from indicators.supertrend import calculate_supertrend



RUNNING = True


latest_candle = None



def shutdown(sig=None, frame=None):

    global RUNNING

    print()
    print("==============================")
    print("[BOT STOPPING]")
    print("==============================")

    RUNNING = False



signal.signal(
    signal.SIGINT,
    shutdown
)



# ============================
# CANDLE CALLBACK
# ============================

def on_candle(candle):

    global latest_candle

    latest_candle = candle


    print("[CANDLE]", candle)



    try:

        indicator = {

            "vwap":
                calculate_vwap(
                    candle
                ),

            "trend":
                calculate_supertrend(
                    candle
                )

        }



        print(
            "[INDICATOR]",
            "PRICE:",
            candle["close"],
            "VWAP:",
            indicator["vwap"],
            "TREND:",
            indicator["trend"]
        )



        signal = strategy_engine.on_candle(
            candle,
            indicator
        )



        execute_signal(
            signal
        )



    except Exception as e:

        print(
            "[STRATEGY ERROR]",
            e
        )




# ============================
# ORDER EXECUTION
# ============================


def execute_signal(signal):


    qty = "0.001"



    if signal == "BUY":


        print(
            "[EXECUTE BUY]"
        )


        result = order_manager.create_order(

            side="Buy",
            qty=qty

        )


        print(
            "[ORDER RESULT]",
            result
        )



    elif signal == "SELL":


        print(
            "[EXECUTE SELL]"
        )


        result = order_manager.create_order(

            side="Sell",
            qty=qty

        )


        print(
            "[ORDER RESULT]",
            result
        )



# ============================
# MAIN
# ============================


def main():


    print("==============================")
    print("VWAP SUPERTREND BOT START")
    print("LIVE :", LIVE_TRADING)
    print("SYMBOL :", DEFAULT_SYMBOL)
    print("BASE :", BYBIT_BASE_URL)
    print("==============================")


    print(
        "[ACCOUNT EQUITY]",
        wallet.get_equity()
    )



    websocket_client.callback = on_candle



    threading.Thread(
        target=websocket_client.start,
        daemon=True
    ).start()



    threading.Thread(
        target=private_ws_client.start,
        daemon=True
    ).start()



    print(
        "[START] STRATEGY LOOP"
    )



    while RUNNING:


        time.sleep(1)



    websocket_client.stop()

    private_ws_client.stop()


    print(
        "[BOT STOPPED]"
    )




if __name__ == "__main__":

    main()
