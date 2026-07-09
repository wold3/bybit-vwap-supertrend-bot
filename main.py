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




RUNNING = True



# ==============================
# RISK SETTINGS
# ==============================

ORDER_QTY = "0.001"


TP_PERCENT = 0.003     # 0.3%

SL_PERCENT = 0.002     # 0.2%





# ==============================
# SHUTDOWN
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
# ORDER EXECUTION
# ==============================


def execute_signal(
        signal,
        price
):


    if not signal:

        return




    print("==============================")
    print("[SIGNAL]", signal)
    print("[PRICE]", price)
    print("==============================")




    # 실제 Bybit 포지션 동기화

    position_manager.sync()



    if position_manager.has_position():

        print(
            "[ORDER BLOCK] POSITION EXISTS",
            position_manager.side(),
            position_manager.size()
        )

        return






    # ==========================
    # BUY
    # ==========================

    if signal == "BUY":



        take_profit = round(

            price *

            (1 + TP_PERCENT),

            1

        )



        stop_loss = round(

            price *

            (1 - SL_PERCENT),

            1

        )



        print(
            "[LONG ENTRY]"
        )


        print(
            "TP:",
            take_profit
        )


        print(
            "SL:",
            stop_loss
        )



        result = order_manager.create_order(

            side="Buy",

            qty=ORDER_QTY,

            take_profit=take_profit,

            stop_loss=stop_loss

        )



        print(
            "[ORDER RESULT]",
            result
        )







    # ==========================
    # SELL
    # ==========================

    elif signal == "SELL":



        take_profit = round(

            price *

            (1 - TP_PERCENT),

            1

        )



        stop_loss = round(

            price *

            (1 + SL_PERCENT),

            1

        )




        print(
            "[SHORT ENTRY]"
        )


        print(
            "TP:",
            take_profit
        )


        print(
            "SL:",
            stop_loss
        )



        result = order_manager.create_order(

            side="Sell",

            qty=ORDER_QTY,

            take_profit=take_profit,

            stop_loss=stop_loss

        )



        print(
            "[ORDER RESULT]",
            result
        )






# ==============================
# CANDLE CALLBACK
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
            "[CANDLE ERROR]",
            e
        )







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





    # Wallet

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





    # 초기 포지션 동기화

    try:


        position_manager.sync()



        print(
            "[CURRENT POSITION]",
            position_manager.current
        )



    except Exception as e:


        print(
            "[POSITION INIT ERROR]",
            e
        )







    # Public WS

    websocket_client.callback = on_candle



    threading.Thread(

        target=websocket_client.start,

        daemon=True

    ).start()






    # Private WS

    threading.Thread(

        target=private_ws_client.start,

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





    # STOP

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
