import os
import json
from dotenv import load_dotenv
import websocket

load_dotenv()

WS_URL = os.getenv(
    "BYBIT_PUBLIC_WS",
    "wss://stream-demo.bybit.com/v5/public/linear"
)

SYMBOL = "BTCUSDT"


def on_open(ws):
    print("[WS CONNECTED]")

    ws.send(json.dumps({
        "op": "subscribe",
        "args": [f"publicTrade.{SYMBOL}"]
    }))


def on_message(ws, message):
    data = json.loads(message)

    if "data" not in data:
        return

    for trade in data["data"]:
        print(
            trade.get("T"),
            trade.get("p"),
            trade.get("v")
        )


def on_error(ws, error):
    print("[WS ERROR]", error)


def on_close(ws, close_status_code, close_msg):
    print("[WS CLOSED]", close_status_code, close_msg)


if __name__ == "__main__":

    websocket.enableTrace(False)

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
