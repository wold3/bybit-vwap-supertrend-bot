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

from position.position_manager import position_manager

from strategy.strategy_engine import strategy_engine

from risk.risk_manager import risk_manager



RUNNING = True



# ==============================
# SETTINGS
# ==============================

ORDER_QTY = "0.001"

TP_PERCENT = 0.003

SL_PERCENT = 0.002





# ==============================
# STOP
# ==============================


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






# ==============================
# ORDER HANDLER
# ==============================


def execute_signal(
        signal_type,
        price
):


    if signal_type is None:

        return





    print("==============================")
    print("[SIGNAL]", signal_type)
    print("[PRICE]", price)
    print("==============================")





    # --------------------------
    # POSITION SYNC
    # --------------------------

    position_manager.sync()



    if position_manager.has_position():

        print(
            "[ORDER BLOCK] POSITION EXISTS",
            position_manager.current
        )


        return






    # --------------------------
    # RISK CHECK
    # --------------------------

    if not risk_manager.allow_order(
            ORDER_QTY
    ):


        print(
            "[ORDER BLOCK] RISK"
        )


        return







    # ==========================
    # BUY
    # ==========================


    if signal_type == "BUY":



        tp = round(

            price *

            (1 + TP_PERCENT),

            1

        )


        sl = round(

            price *

            (1 - SL_PERCENT),

            1

        )



        print("[LONG ENTRY]")


        result = order_manager.create_order(

            side="Buy",

            qty=ORDER_QTY,

            take_profit=tp,

            stop_loss=sl

        )



        print(
            "[ORDER RESULT]",
            result
        )







    # ==========================
    # SELL
    # ==========================


    elif signal_type == "SELL":



        tp = round(

            price *

            (1 - TP_PERCENT),

            1

        )


        sl = round(

            price *

            (1 + SL_PERCENT),

            1

        )



        print("[SHORT ENTRY]")



        result = order_manager.create_order(

            side="Sell",

            qty=ORDER_QTY,

            take_profit=tp,

            stop_loss=sl

        )



        print(
            "[ORDER RESULT]",
            result
        )








# ==============================
# MARKET CALLBACK
# ==============================


def on_candle(candle):


    try:


        print(
            "[CANDLE]",
            candle
        )



        signal_type = strategy_engine.on_candle(

            candle

        )



        execute_signal(

            signal_type,

            candle["close"]

        )




    except Exception as e:


        print(
            "[CANDLE ERROR]",
            e
        )







# ==============================
# POSITION MONITOR
# ==============================


def position_monitor():



    print(
        "[POSITION MONITOR START]"
    )



    while RUNNING:


        try:


            position_manager.sync()



        except Exception as e:


            print(
                "[POSITION MONITOR ERROR]",
                e
            )



        time.sleep(5)







# ==============================
# STRATEGY LOOP
# ==============================


def strategy_loop():



    print(
        "[START] STRATEGY LOOP"
    )



    while RUNNING:


        time.sleep(1)








# ==============================
# MAIN
# ==============================


def main():



    print("==============================")
    print("VWAP SUPERTREND BOT START")
    print("==============================")



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


    print("==============================")







    # --------------------------
    # WALLET
    # --------------------------


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







    # --------------------------
    # INITIAL POSITION
    # --------------------------


    position_manager.sync()



    print(
        "[POSITION INIT]",
        position_manager.current
    )







    # --------------------------
    # RISK
    # --------------------------


    print(
        "[RISK STATUS]",
        risk_manager.status()
    )







    # --------------------------
    # CALLBACK
    # --------------------------


    websocket_client.callback = on_candle







    # --------------------------
    # THREADS
    # --------------------------


    threading.Thread(

        target=websocket_client.start,

        daemon=True

    ).start()



    threading.Thread(

        target=private_ws_client.start,

        daemon=True

    ).start()



    threading.Thread(

        target=position_monitor,

        daemon=True

    ).start()



    threading.Thread(

        target=strategy_loop,

        daemon=True

    ).start()






    print(
        "[BOT RUNNING]"
    )







    while RUNNING:


        time.sleep(1)








    # --------------------------
    # CLEAN STOP
    # --------------------------


    try:

        websocket_client.stop()

    except:

        pass



    try:

        private_ws_client.stop()

    except:

        pass



    print(
        "[BOT STOPPED]"
    )








if __name__ == "__main__":

    main()
