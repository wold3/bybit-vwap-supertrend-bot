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
# ORDER SETTINGS
# ==============================


ORDER_QTY = "0.001"


TP_PERCENT = 0.003

SL_PERCENT = 0.002





# ==============================
# SIGNAL STOP
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
# ORDER PROCESS
# ==============================


def execute_signal(
        trade_signal,
        price
):


    if trade_signal is None:

        return




    print("==============================")
    print("[SIGNAL]", trade_signal)
    print("[PRICE]", price)
    print("==============================")





    # --------------------------
    # Position check
    # --------------------------


    try:

        position_manager.sync()


    except Exception as e:

        print(
            "[POSITION SYNC ERROR]",
            e
        )




    if position_manager.has_position():


        print(
            "[ORDER BLOCK] POSITION EXISTS"
        )


        return





    # --------------------------
    # Risk check
    # --------------------------


    if not risk_manager.allow_order(
            ORDER_QTY
    ):


        print(
            "[ORDER BLOCK] RISK"
        )


        return





    # --------------------------
    # BUY
    # --------------------------


    if trade_signal == "BUY":



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



        print(
            "[LONG ENTRY]"
        )



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







    # --------------------------
    # SELL
    # --------------------------


    elif trade_signal == "SELL":



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



        print(
            "[SHORT ENTRY]"
        )



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



        signal = strategy_engine.on_candle(

            candle

        )



        execute_signal(

            signal,

            candle["close"]

        )




    except Exception as e:


        print(
            "[STRATEGY ERROR]",
            e
        )







# ==============================
# LOOP
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
    # Wallet
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
    # Position
    # --------------------------


    try:


        position_manager.sync()



        print(
            "[POSITION]",
            position_manager.current
        )



    except Exception as e:


        print(
            "[POSITION INIT ERROR]",
            e
        )







    # --------------------------
    # Risk
    # --------------------------


    print(

        "[RISK STATUS]",

        risk_manager.status()

    )







    # --------------------------
    # PUBLIC WS
    # --------------------------


    websocket_client.callback = on_candle



    threading.Thread(

        target=websocket_client.start,

        daemon=True

    ).start()







    # --------------------------
    # PRIVATE WS
    # --------------------------


    threading.Thread(

        target=private_ws_client.start,

        daemon=True

    ).start()






    # --------------------------
    # Strategy
    # --------------------------


    threading.Thread(

        target=strategy_loop,

        daemon=True

    ).start()






    print(
        "[BOT RUNNING]"
    )






    while RUNNING:


        time.sleep(1)






    # shutdown


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
