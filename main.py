import time
import threading


from config import (
    LIVE_TRADING,
    DEFAULT_SYMBOL
)


from market.websocket_client import public_ws
from services.private_ws_client import private_ws_client

from portfolio.bybit_wallet import wallet

from execution.order_manager import order_manager


from strategy.strategy_engine import (
    strategy_engine
)



# ======================================
# BOT STATE
# ======================================

running = True


position = {

    "side": None,

    "qty": 0

}



# ======================================
# RISK SETTINGS
# ======================================

TP_PERCENT = 0.003     # +0.3%
SL_PERCENT = 0.002     # -0.2%


ORDER_QTY = "0.001"




# ======================================
# POSITION CHECK
# ======================================


def has_position():


    if position["side"]:

        return True


    return False




# ======================================
# ORDER EXECUTION
# ======================================


def execute_signal(signal, price):


    global position



    print("==============================")
    print("[SIGNAL]")
    print(signal)
    print("PRICE :", price)
    print("==============================")




    # ----------------------------
    # 중복 진입 방지
    # ----------------------------

    if has_position():

        print(
            "[SKIP] POSITION EXISTS"
        )

        return





    # ----------------------------
    # LONG ENTRY
    # ----------------------------

    if signal == "BUY":



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


        print(
            "TP:",
            tp
        )


        print(
            "SL:",
            sl
        )



        result = order_manager.create_order(

            side="Buy",

            qty=ORDER_QTY,

            take_profit=tp,

            stop_loss=sl

        )




        if result and result.get(
            "retCode"
        ) == 0:


            position["side"] = "Buy"

            position["qty"] = ORDER_QTY


            print(
                "[POSITION OPEN]"
            )






    # ----------------------------
    # SHORT ENTRY
    # ----------------------------

    elif signal == "SELL":



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





        if result and result.get(
            "retCode"
        ) == 0:


            position["side"] = "Sell"

            position["qty"] = ORDER_QTY


            print(
                "[POSITION OPEN]"
            )





# ======================================
# CANDLE CALLBACK
# ======================================


def on_candle(candle):


    price = candle["close"]



    signal = strategy_engine.on_candle(

        candle

    )



    if signal:


        execute_signal(

            signal,

            price

        )





# ======================================
# STRATEGY LOOP
# ======================================


def strategy_loop():


    print(
        "[START] STRATEGY LOOP"
    )


    while running:


        time.sleep(1)





# ======================================
# START
# ======================================


def main():



    print("====================================")
    print("VWAP SUPERTREND BOT START")
    print("LIVE :", LIVE_TRADING)
    print("SYMBOL :", DEFAULT_SYMBOL)
    print("====================================")



    print(
        "[WATCHDOG START]"
    )



    # public websocket

    public_ws.start(

        callback=on_candle

    )



    # private websocket

    private_ws_client.start()



    threading.Thread(

        target=strategy_loop,

        daemon=True

    ).start()





    try:


        while True:

            time.sleep(1)



    except KeyboardInterrupt:


        print(
            "\n[BOT STOPPING]"
        )



        public_ws.stop()

        private_ws_client.stop()



        print(
            "[BOT STOPPED]"
        )






if __name__ == "__main__":


    main()
