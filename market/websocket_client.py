import os
import json
import time
import websocket

from dotenv import load_dotenv

from market.candle_builder import candle_builder
from strategy.vwap_supertrend_strategy import vwap_supertrend_strategy
from execution.execution_engine import execution_engine


load_dotenv()


WS_URL = os.getenv(
    "BYBIT_PUBLIC_WS",
    "wss://stream-demo.bybit.com/v5/public/linear"
)


SYMBOL = "BTCUSDT"



# =====================================
# WS OPEN
# =====================================

def on_open(ws):

    print("[WS CONNECTED]")


    subscribe = {

        "op": "subscribe",

        "args": [

            f"publicTrade.{SYMBOL}"

        ]

    }


    ws.send(
        json.dumps(subscribe)
    )


    print(
        "[SUBSCRIBED]",
        SYMBOL
    )




# =====================================
# MESSAGE
# =====================================

def on_message(
    ws,
    message
):


    try:

        data = json.loads(
            message
        )


    except:

        return



    if "data" not in data:

        return



    for trade in data["data"]:


        price = float(
            trade["p"]
        )


        volume = float(
            trade["v"]
        )



        # ==========================
        # TICK -> CANDLE
        # ==========================

        closed = candle_builder.update(

            SYMBOL,

            price,

            volume

        )



        if closed:


            print(
                "[CANDLE CLOSED]",
                closed
            )



            candles = candle_builder.get_candles(

                SYMBOL

            )



            signal = vwap_supertrend_strategy.analyze(

                candles

            )



            if signal:


                print(
                    "[SIGNAL]",
                    signal
                )


                signal["symbol"] = SYMBOL


                signal["qty"] = 0.001



                result = execution_engine.execute_signal(

                    signal

                )


                print(
                    "[ORDER RESULT]",
                    result
                )




# =====================================
# ERROR
# =====================================

def on_error(
    ws,
    error
):

    print(
        "[WS ERROR]",
        error
    )




# =====================================
# CLOSE
# =====================================

def on_close(
    ws,
    code,
    msg
):

    print(
        "[WS CLOSED]",
        code,
        msg
    )




# =====================================
# RUN
# =====================================

def start():


    while True:


        try:


            ws = websocket.WebSocketApp(

                WS_URL,

                on_open=on_open,

                on_message=on_message,

                on_error=on_error,

                on_close=on_close

            )


            ws.run_forever(

                ping_interval=20,

                ping_timeout=10

            )


        except Exception as e:


            print(
                "[RECONNECT ERROR]",
                e
            )


        print(
            "[RECONNECTING...]"
        )


        time.sleep(5)





if __name__ == "__main__":

    websocket.enableTrace(False)

    start()
